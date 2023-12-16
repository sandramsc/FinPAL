from dotenv import load_dotenv

load_dotenv()
from fastapi.responses import RedirectResponse

from libs.telegram import Telegram
from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


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


@app.post("/telegram_webhook")
async def telegram_webhook(request: Request) -> None:
    parsed_request = await request.json()
    # telegram = Telegram(parsed_request=parsed_request)
    # await telegram.send_message("Hello, I'm a bot!")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
