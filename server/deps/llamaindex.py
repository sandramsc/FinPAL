from llama_index.llms import Gemini, OpenAI
from llama_index.multi_modal_llms import GeminiMultiModal
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY is not set")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is not set")

GeminiPro = Gemini(model_name="models/gemini-pro", api_key=GOOGLE_API_KEY)

# GeminiProVision = GeminiMultiModal(api_key=GOOGLE_API_KEY, model_name="gemini-pro-vision")

GPT35_Turbo = OpenAI(model_name="gpt-3.5-turbo-1106",api_key=OPENAI_API_KEY)

