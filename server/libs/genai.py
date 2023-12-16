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

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# model = genai.GenerativeModel(
#     model_name="gemini-pro",
#     generation_config=generation_config,
#     safety_settings=safety_settings,
# )
# model = genai.GenerativeModel("gemini-pro")

# messages = [{'role':'user', 'parts': ['hello, tell me a story of a bread']}]
# response = model.generate_content(contents=messages, stream=True) # "Hello, how can I help"
# for res in response:
#     print(res.text)
# messages.append(response.candidates[0].content)
# messages.append({'role':'user', 'parts': ['How does quantum physics work?']})
# response = model.generate_content(messages)
# print("chat_history1",chat.history)
# print(chat.send_message(content="hello"))

# print("chat_history2",chat.history)
# print(chat.history)
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