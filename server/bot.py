#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from dotenv import load_dotenv
load_dotenv()
import os
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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
Or
You can sync your financial data through Plaid to us.
I can analyze your spending, income, help you save money and attain your financial goal.
I can also generate graphs and help you visualize your financial data.

Oh wait, I can also create a reminder to remind you about your budget.
Want to get real time update on any financial news ? stock price ? I can help you.
""",
        reply_markup=ForceReply(selective=True),
    )
    # create user_id in DB
    from libs.prisma import db
    await db.connect()
    db_user = await db.user.upsert(
        where={"telegramId": str(user.id),},
        data={
            "create":{
                "telegramId": str(user.id),
                "telegramThread":{
                    "create":{
                        "platform": "telegram",
                    }
                }
            },
            "update":{
                "telegramId": str(user.id),
            }
        }
    )
    await db.disconnect()
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
    thread_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    message = update.effective_message.text
    from libs.agent import Agent
    agent = Agent(thread_id=str(thread_id))
    # create an empty message
    loading = await update.message.reply_markdown_v2(text="_typing_ \.\.\.")
    streaming = agent.run(message_content=message)
    async for progress in streaming:
        print("progress",progress.content)
        await loading.edit_text(text=progress.content)
    

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()