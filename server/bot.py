#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.


import logging
from typing import Any
from dotenv import load_dotenv
import nest_asyncio

# 👇️ call apply()
nest_asyncio.apply()
load_dotenv()
import os
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN is not set")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"""Hi {user.mention_html()}!
I'm finPAL, your financial helper.
I can analyze your financial data and help you with your financial goals.
You can start by uploading your financial data.
I can analyze your spending, income, help you save money and attain your financial goal.
I can also generate graphs and help you visualize your financial data.
""",
    )
    # create user_id in DB
    from libs.prisma import db

    thread_id = update.effective_chat.id
    print("userid threadid", thread_id, user.id)
    db_user = db.user.upsert(
        where={
            "telegramId": str(user.id),
        },
        data={
            "create": {
                "telegramThread": {
                    "create": {
                        "platform": "telegram",
                        "id": str(thread_id),
                    }
                },
                "telegramId": str(user.id),
            },
            "update": {"telegramId": str(user.id)},
        },
    )
    # we will continue tracking the state of the user in the DB
    # each conversation through agent will be tracked in the DB


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def agent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # thread id is similar to user id in this case
    user_id = update.effective_user.id
    thread_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    message = update.effective_message.text
    photo = update.effective_message.photo
    from telegram.constants import ChatAction

    await context.bot.send_chat_action(chat_id=thread_id, action=ChatAction.TYPING)

    if len(photo) > 0:
        photo = await photo[-1].get_file()
        photo = await photo.download_as_bytearray()

    from libs.agent import Agent

    # # create an empty message
    # loading = await update.message.reply_markdown(text="_typing_ _..._")
    from libs.prisma import db

    db_user = db.user.find_unique(
        where={
            "telegramId": str(user_id),
        }
    )

    # retrieve today datetime for bot context

    from datetime import datetime

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    SYSTEM_PROMPT = f"""
You are a helpful assistant.
Your name is FinPal.
You put emoji everywhere.
When user sent a receipt, ask first for confirmation of the transaction data before saving it.
You encourage people to set financial goal, and help them achieve their financial goal.
You can store user transaction from user photo.
You can analyze user finance, networth, savings, spending, budget, etc.
You can also generate graphs and help user visualize their financial data.
You want to collect user transaction data, because with more data you can create analyze their finance better and create a better budget planning.
Today datetime is {dt_string}
    """

    await context.bot.send_chat_action(chat_id=thread_id, action=ChatAction.TYPING)
    agent = Agent(
        thread_id=str(thread_id), user_id=db_user.id, system_prompt=SYSTEM_PROMPT
    )

    from libs.typings import Message

    # using this to wrap async streaming agent into async agent
    async def agent_wrapper(message):
        streaming = agent.run(
            input=Message(
                content=message,
                role="user",
                photo=photo if type(photo) == bytearray else None,
            )
        )
        result = ""
        # from telegram.constants import ParseMode
        async for progress in streaming:
            print("progress", progress)
            await update.message.reply_markdown(text=progress.content)
            result = progress.content
        return result

    def sync_wrapper(message: str):
        import asyncio

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(agent_wrapper(message=message))
        return result
    
    from trulens_eval import Feedback, OpenAI as fOpenAI
    # synchronize_async_helper(agent_wrapper, message)
    # initialize feedback
    # Initialize OpenAI-based feedback function collection class:
    fopenai = fOpenAI()

    # Define a relevance function from openai
    f_relevance = Feedback(fopenai.relevance_with_cot_reasons).on_input_output()
    # f_conciseness = Feedback(fopenai.conciseness_with_cot_reasons).on_output()
    # f_correctness = Feedback(fopenai.coherence_with_cot_reasons).on_output()
    f_helpfulness = Feedback(fopenai.helpfulness_with_cot_reasons).on_output()
    from trulens_eval import TruBasicApp

    tru_llm_standalone_recorder = TruBasicApp(
        sync_wrapper,
        app_id="finPalv1",
        feedbacks=[f_relevance, f_helpfulness],
    )

    with tru_llm_standalone_recorder as recording:
        tru_llm_standalone_recorder.app(message=message)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent))
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, agent))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
