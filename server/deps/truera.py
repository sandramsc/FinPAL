from dotenv import load_dotenv
import os

load_dotenv()

# initialize truera
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru

tru = Tru(
    # database_url=os.getenv("TRUERA_DATABASE_URL"),
)
