import os

from openai import OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

from IPython.display import JSON

# Create openai client
from openai import OpenAI
client = OpenAI()

# Imports main tools:
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru
tru = Tru()
tru.reset_database()