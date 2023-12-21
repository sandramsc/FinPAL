from openai import AsyncOpenAI
import os
import instructor
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is not set")

openai = instructor.apatch(AsyncOpenAI(api_key=OPENAI_API_KEY))
