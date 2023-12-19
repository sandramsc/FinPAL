# THIS WILL BE THE HIGH LEVEL LOGIC OF AGENT WITHOUT LOW LEVEL API DETAILS
import json
from typing import AsyncIterable, Iterable, Literal, Optional
from openai import AsyncStream
from pydantic import BaseModel
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall

SYSTEM_PROMPT = """
Develop a conversational system prompt for a financial assistant named finPAL. 
finPAL is designed to analyze users' financial data and assist with their financial goals. 
It should encourage users to upload their financial data via photo.
The prompt should highlight finPAL's capabilities, such as analyzing spending, income, helping with savings, generating graphs, visualizing financial data, setting budget reminders.
The tone should be informative and engaging.
Add a lot of emoji.
Reply in markdown format.
Don't make up stuff !
"""
from libs.typings import Message
from libs.tools.index import openai_tools
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

class Agent:
    def __init__(
        self, thread_id: str, user_id=str, system_prompt=SYSTEM_PROMPT, tools=openai_tools
    ) -> None:
        self.system_prompt = system_prompt
        self.thread_id = thread_id
        self.tools = tools
        self.user_id = user_id
        pass

    # async def messages(self) -> list[Message]:
    #     from libs.prisma import db

    #     await db.connect()
    #     # retrieve messages from DB
    #     db_messages = await db.message.find_many(
    #         where={"threadId": self.thread_id}, take=5, order={"createdAt": "asc"}
    #     )
    #     await db.disconnect()
    #     parsed_messages = []
    #     for message in db_messages:
    #         parsed_messages.append(
    #             Message(role="assistant" if message.isBot else "user")
    #         )
    #     return parsed_messages

    # async def run(self, message_content: str) -> AsyncIterable[Message]:
    #     messages = await self.messages()

    #     # add system prompt at the end
    #     messages.append(Message(content=self.system_prompt, role="system"))

    #     # add user message
    #     messages.append(Message(content=message_content, role="user"))

    #     # get prediction
    #     from libs.genai import GeminiPro

    #     model = GeminiPro()

    #     res = model.achat(messages=messages)

    #     # we send the streaming response
    #     complete_text = ""
    #     async for chunk in res:
    #         complete_text += chunk

    #         yield Message(content=complete_text, role="assistant")

    async def messages(self) -> list[Message]:
        from libs.prisma import db

        # retrieve messages from DB
        db_messages = db.message.find_many(
            where={"threadId": self.thread_id}, take=5, order={"createdAt": "asc"}
        )

        parsed_messages = []
        for message in db_messages:
            parsed_messages.append(
                Message(
                    content=message.text, role="assistant" if message.isBot else "user"
                )
            )
        return parsed_messages
    
    async def truncate_messages(self, messages: list[Message])->list[Message]:
        pass

    async def input_parser(self, input: Message) -> Message:
        # TODO: dynamically generate prompt for the multimodal prompt
        from libs.genai import GeminiProVision

        PROMPT = """
        Describe the image in detail. Don't make up stuff !
        """

        if input.photo:
            gemini = GeminiProVision()
            res = gemini.apredict(files=[input.photo], text=PROMPT)
            output = "Please store this receipt in the database : \n"
            async for r in res:
                output += r
            input.content = output

        # save to DB
        from libs.prisma import db
        
        db_message = db.message.create(
            data={
                "isBot":False,
                "photo":"not saved to db",
                "text":input.content,
                "threadId":self.thread_id
            }
        )
        print("db_message", db_message)
        return Message(content=input.content, role="user")

    async def run(self, input: Message) -> AsyncIterable[Message]:
        # this messages object will be mutated throughout the run
        messages = await self.messages()

        # add system prompt at the end
        messages.append(Message(content=self.system_prompt, role="system"))

        # parse user message
        parsed_input = await self.input_parser(input=input)

        # add user message
        messages.append(Message(content=parsed_input.content, role="user"))
        self.run_left = 1
        while self.run_left > 0:
            self.run_left -= 1
            # iterate the run
            run_step_output = await self.run_step(input=messages)
            # remove 1st message to maintain context window
            # TODO: use truncation and summarization
            # messages.pop(0)

            # send newly generated message
            for new_message in run_step_output:
                yield await self.output_parser(new_message)

    async def run_step(self, input: list[Message]) -> list[Message]:
        from libs.openai import openai

        res = await openai.chat.completions.create(
            messages=input, model="gpt-3.5-turbo-1106", tools=self.tools, presence_penalty=2
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
                    input.append(Message(tool_call_id=tool_call_res.tool_call_id, role=tool_call_res.role, name=tool_call_res.name,content=tool_call_res.content))
            else:
                parsed_output.append(Message(content=text_response, role="assistant"))
        return parsed_output

    async def execute_tools(self, input: list[ChatCompletionMessageToolCall]) -> list[Message]:
        from libs.tools.index import TOOLS
        messages = []
        for tool_call in input:
            tool_name = tool_call.function.name
            fn = TOOLS[tool_name]["fn"]
            tool_args = json.loads(tool_call.function.arguments)
            # this will return a pydantic class
            input_schema = TOOLS[tool_name]["schema"]
            response = await fn(input= input_schema(**tool_args), user_id = self.user_id)
            messages.append(Message(content=response, role="tool",name=tool_name, tool_call_id=tool_call.id))

        return messages
    
    async def output_parser(self, output: Message) -> Message:
        # save output to db
        from libs.prisma import db
        
        db_message = db.message.create(
            data={
                "text":output.content,
                "isBot":True,
                "threadId":self.thread_id
            }
        )
        
        # TODO: add more output parser as needed
        return Message(content=output.content, role="assistant")

    def logger(self, log_name: str, log_object: str):
        print(f"logger -> {log_name} -> ", log_object)