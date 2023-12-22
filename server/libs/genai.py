from typing import Any, AsyncIterable, Literal, Optional
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

    def input_parser(self, messages: list[Message]) -> list[dict]:
        parsed_messages = []
        for message in messages:
            parsed_messages.append(
                {
                    "role": "user" if message.role == "user" else "model",
                    "parts": [message.content] if message.content else [],
                }
            )
        print("parsed_messages", parsed_messages)
        return parsed_messages

    async def achat(self, messages: list[dict]) -> AsyncIterable[str]:
        
        parsed_messages = self.input_parser(messages)
        res = self.model.generate_content(contents=parsed_messages, stream=True)
        for chunk in res:
            yield chunk.text


class GeminiProVision:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel(model_name="gemini-pro-vision")

    def input_parser(
        self, files: [bytes], text: Optional[str] = None
    ) -> list[dict | str]:
        parsed_input = []
        for file in files:
            parsed_input.append(
                {"mime_type": "image/jpeg", "data": file},
            )
        # add text
        if text:
            parsed_input.append(text)
        return parsed_input

    async def apredict(self, files: [bytes], text: Optional[str] = None) -> AsyncIterable[str]:
        generation_config = {
            "max_output_tokens": 4096,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        parsed_input = self.input_parser(files=files, text=text)
        res = self.model.generate_content(contents=parsed_input, stream=True,generation_config=generation_config,safety_settings=safety_settings)
        for r in res:
            for part in r.parts:
                yield part.text