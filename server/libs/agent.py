# THIS WILL BE THE HIGH LEVEL LOGIC OF AGENT WITHOUT LOW LEVEL API DETAILS
from typing import AsyncIterable, Literal, Optional
from pydantic import BaseModel


SYSTEM_PROMPT = """
Develop a conversational system prompt for a financial assistant named finPAL. 
finPAL is designed to analyze users' financial data and assist with their financial goals. 
It should encourage users to upload their financial data or sync it through Plaid. 
The prompt should highlight finPAL's capabilities, such as analyzing spending, income, helping with savings, generating graphs, visualizing financial data, setting budget reminders, and providing real-time updates on financial news and stock prices. 
The tone should be informative and engaging.
"""
from libs.typings import Message


class Agent:
    def __init__(self, thread_id: str, system_prompt=SYSTEM_PROMPT) -> None:
        self.system_prompt = system_prompt
        self.thread_id = thread_id
        pass

    async def messages(self) -> list[Message]:
        from libs.prisma import db

        await db.connect()
        # retrieve messages from DB
        db_messages = await db.message.find_many(
            where={"threadId": self.thread_id}, take=5, order={"createdAt": "asc"}
        )
        await db.disconnect()
        parsed_messages = []
        for message in db_messages:
            parsed_messages.append(
                Message(role="assistant" if message.isBot else "user")
            )
        return parsed_messages

    async def run(self, message_content: str) -> AsyncIterable[Message]:
        messages = await self.messages()

        # # add system prompt at the end
        # messages.append(Message(content=self.system_prompt, role="system"))

        # add user message
        messages.append(Message(content=message_content, role="user"))

        # get prediction
        from libs.genai import GeminiPro

        model = GeminiPro()

        res = model.achat(messages=messages)

        # we send the streaming response
        text_chunk = ""
        async for chunk in res:
            text_chunk += chunk
            yield Message(content=text_chunk, role="assistant")

    def logger(self, log_object=str):
        print("logger", log_object)

