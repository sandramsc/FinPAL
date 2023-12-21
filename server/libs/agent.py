# THIS WILL BE THE HIGH LEVEL LOGIC OF AGENT WITHOUT LOW LEVEL API DETAILS
import json
from typing import AsyncIterable, Iterable, Literal, Optional
from openai import AsyncStream
from pydantic import BaseModel
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)

SYSTEM_PROMPT = """
You are a helpful assistant.
Your name is FinPal.
Your task is to improve user's financial situation.
You like to use emojis.
You always reply in markdown format.
You can analyze user finance, networth, savings, spending, budget, etc.
You can also generate graphs and help user visualize their financial data.
You want to collect user transaction data, because with more data you can create analyze their finance better and create a better budget planning.
"""
from libs.typings import Message
from libs.tools.index import openai_tools
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


class Agent:
    def __init__(
        self,
        thread_id: str,
        user_id=str,
        system_prompt=SYSTEM_PROMPT,
        tools=openai_tools,
        model_max_token=16385,
    ) -> None:
        self.system_prompt = system_prompt
        self.thread_id = thread_id
        self.tools = tools
        self.user_id = user_id
        self.model_max_token = model_max_token
        self.max_response_token = int(self.model_max_token / 9)
        self.max_context_token = int(self.model_max_token - self.max_response_token)
        pass

    async def messages(self) -> list[Message]:
        """
        Retrieves a list of messages associated with the current thread.

        Returns:
            list[Message]: A list of Message objects representing the retrieved messages.
        """
        from libs.prisma import db

        # retrieve messages from DB
        # reversed because we want oldest messages at the top, newest at the bottom
        db_messages = db.message.find_many(
            where={"threadId": self.thread_id}, take=20, order={"createdAt": "desc"}
        )

        reversed_db_messages = db_messages[::-1]
        parsed_messages = []
        for message in reversed_db_messages:
            parsed_messages.append(
                Message(
                    content=message.text, role="assistant" if message.isBot else "user"
                )
            )
        # add system prompt at the end to enforce prompt
        parsed_messages.append(Message(content=self.system_prompt, role="system"))

        return parsed_messages

    async def truncate_messages(self, messages: list[Message]) -> list[Message]:
        import tiktoken

        encoding = tiktoken.get_encoding("cl100k_base")
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
        context_token_left = self.max_context_token

        # calculate tools token
        for tool in self.tools:
            tool_token = len(encoding.encode(json.dumps(tool)))
            context_token_left -= tool_token
        # we will start counting token from the newest messages (bottom / last), and truncate the oldest one (1st / top)
        index = len(messages) - 1
        while index >= 0 and context_token_left >= 0:
            message = messages[index]
            token = len(encoding.encode(message.model_dump_json()))
            context_token_left -= token
            index -= 1

        # we truncate messages based on index
        messages = messages[index + 1 :]
        return messages

    async def input_parser(self, input: Message) -> Message:
        # TODO: dynamically generate prompt for the multimodal prompt
        from libs.genai import GeminiProVision

        output = input.content
        PROMPT = """
        Given an image or images, write a detailed description of the image. Don't make up stuff.
        Objects: Mention all available object in the images, the size, the brand, the colour, etc.
        Text: Mention all the text in the image and on what object it's written on.
        
        If it's a receipt, extract all the information from the receipt.
            "amountIn": 0
            "amountOut": 20.56
            "category": 'Grocery', 'FoodAndDining', 'RentAndMortgage', 'Utilities', 'Transportation', 'Entertainment', 'Healthcare', 'Clothing', 'Education' or 'Miscellaneous'
            "transactionDate": yyyymmdd
            "currency": USD
            "description": 
            "sourceOrPayee": 
        """

        if input.photo:
            gemini = GeminiProVision()
            res = gemini.apredict(files=[input.photo], text=PROMPT)
            output = "This is a parsed message of the actual user message containing an image. Here's the description of the image : \n"
            async for r in res:
                output += r
            print("output", output)

        # save to DB
        from libs.prisma import db

        db_message = db.message.create(
            data={
                "isBot": False,
                "photo": "not saved to db",
                "text": output,
                "threadId": self.thread_id,
            }
        )

        return Message(content=output, role="user")

    async def run(self, input: Message) -> AsyncIterable[Message]:
        # this messages object will be mutated throughout the run
        messages = await self.messages()

        # parse user message
        parsed_input = await self.input_parser(input=input)

        # add user message
        messages.append(Message(content=parsed_input.content, role="user"))

        # truncate messages
        messages = await self.truncate_messages(messages=messages)
        print(messages)
        self.run_left = 1
        while self.run_left > 0:
            self.run_left -= 1
            # iterate the run
            run_step_output = await self.run_step(input=messages)
            # remove 1st message to maintain context window

            messages.pop(0)

            # send newly generated message
            for new_message in run_step_output:
                yield await self.output_parser(new_message)

    async def run_step(self, input: list[Message]) -> list[Message]:
        from libs.openai import openai

        res = await openai.chat.completions.create(
            messages=input,
            model="gpt-3.5-turbo-1106",
            tools=self.tools,
            presence_penalty=2,
            max_tokens=self.max_response_token,
            frequency_penalty=2,
            temperature=0.2
        )
        res_messages = res.choices

        parsed_output = []
        for res_message in res_messages:
            text_response = res_message.message.content
            tool_calls = res_message.message.tool_calls
            # append 1st response to message
            if tool_calls and len(tool_calls) > 0:
                self.run_left += 1

                # add toolcall to message
                input.append(res_message.message)

                tool_calls_res = await self.execute_tools(input=tool_calls)

                # append tool_call_res to message
                for tool_call_res in tool_calls_res:
                    input.append(
                        Message(
                            tool_call_id=tool_call_res.tool_call_id,
                            role=tool_call_res.role,
                            name=tool_call_res.name,
                            content=tool_call_res.content,
                        )
                    )
            else:
                parsed_output.append(Message(content=text_response, role="assistant"))
        return parsed_output

    async def execute_tools(
        self, input: list[ChatCompletionMessageToolCall]
    ) -> list[Message]:
        from libs.tools.index import TOOLS

        messages = []
        for tool_call in input:
            try:
                tool_name = tool_call.function.name
                fn = TOOLS[tool_name]["fn"]
                tool_args = json.loads(tool_call.function.arguments)
                # this will return a pydantic class
                input_schema = TOOLS[tool_name]["schema"]
                response = await fn(
                    input=input_schema(**tool_args), user_id=self.user_id
                )
                messages.append(
                    Message(
                        content=response,
                        role="tool",
                        name=tool_name,
                        tool_call_id=tool_call.id,
                    )
                )
            except Exception as e:
                print(e)
                self.run_left += 1
                messages.append(
                    Message(
                        content=f"Error: {e}",
                        role="tool",
                        name=tool_name,
                        tool_call_id=tool_call.id,
                    )
                )
        return messages

    async def output_parser(self, output: Message) -> Message:
        # save output to db
        from libs.prisma import db

        db_message = db.message.create(
            data={"text": output.content, "isBot": True, "threadId": self.thread_id}
        )

        # TODO: add more output parser as needed
        return Message(content=output.content, role="assistant")

    def logger(self, log_name: str, log_object: str):
        print(f"logger -> {log_name} -> ", log_object)
