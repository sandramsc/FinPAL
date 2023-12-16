from typing import Annotated, AsyncIterable, Iterable
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
 
from llama_index.llms import Gemini,ChatMessage
from llama_index.multi_modal_llms.gemini import GeminiMultiModal

from llama_index.multi_modal_llms.generic_utils import (
    load_image_urls,
)

image_urls = [
    "https://storage.googleapis.com/generativeai-downloads/data/scene.jpg",
    # Add yours here!
]

image_documents = load_image_urls(image_urls)

gemini_pro = GeminiMultiModal(model="models/gemini-pro",api_key=GOOGLE_API_KEY)
