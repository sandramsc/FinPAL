"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from typing import Any, AsyncIterable, Literal
import google.generativeai as genai
from google.generativeai.types.content_types import ContentDict

import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


from libs.typings import Message

class GeminiPro:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel("gemini-pro")

    def input_parser(self, messages:list[Message]) -> list[dict]:
        parsed_messages = []
        for message in messages:
            parsed_messages.append({
                "role": "user" if message.role == "user" else "model",
                "parts": [message.content] if message.content else []
            })
        print("parsed_messages", parsed_messages)
        return parsed_messages
     
    async def achat(self, messages: list[dict]) -> AsyncIterable[str]:
        parsed_messages = self.input_parser(messages)
        res = self.model.generate_content(contents=parsed_messages, stream=True)
        for chunk in res:
            print(chunk.text)
            yield chunk.text

# class GeminiProVision:
#     def __init__(self, api_key=GOOGLE_API_KEY) -> None:
#         self.model = genai.GenerativeModel(model_name="gemini-pro-vision")

#     async def apredict(self, messages: list[dict]) -> AsyncIterable[str]:
#         parsed_messages = self.input_parser(messages)
#         res = self.model.generate_content(contents=parsed_messages, stream=True)
#         for r in res:
#             yield r.text

# model = GeminiPro()