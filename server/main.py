from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
import httpx

load_dotenv()
import os
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")

if not TELEGRAM_BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN is not set")

if not SERVER_URL:
    raise Exception("SERVER_URL is not set")

# init webhook
httpx.get(
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={SERVER_URL}/telegram_webhook"
)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return RedirectResponse("/docs")


@app.get("/telegram_webhook")
async def telegram_webhook():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
