import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from libs.llamaindex import pydantic_gemini
from instructor import OpenAISchema


class SaveTransactionToDB(OpenAISchema):
    "Save user transaction into database"
    amountOut: str = None
    amountIn: str = None
    currency: str
    sourceOrPayee: str = None
    category: Literal[
        "Grocery",
        "FoodAndDining",
        "RentAndMortgage",
        "Utilities",
        "Transportation",
        "Entertainment",
        "Healthcare",
        "Clothing",
        "Education",
        "Miscellaneous",
    ] = "Miscellaneous"
    description: str = None
    transactionDate: Annotated[str, Field(description="yyyymmdd")] = None


async def save_transaction_to_db(input: SaveTransactionToDB, user_id: str):
    from libs.prisma import db
    # save data to db
    db_transaction = db.transaction.create(
        data={
            "amountIn": input.amountIn,
            "amountOut": input.amountOut,
            "category": input.category,
            "transactionDate": input.transactionDate,
            "currency": input.currency,
            "description": input.description,
            "sourceOrPayee": input.sourceOrPayee,
            "userId": user_id,
        }
    )
    print("db_transaction",db_transaction)
    return db_transaction.model_dump_json()


TOOLS = {
    "SaveTransactionToDB": {"fn": save_transaction_to_db, "schema": SaveTransactionToDB}
}

openai_tools = []
for tool_name in TOOLS:
    tool_schema = TOOLS[tool_name]["schema"].openai_schema
    openai_tools.append({"type": "function", "function": tool_schema})
