import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from libs.llamaindex import pydantic_gemini
from instructor import OpenAISchema


class SaveTransactionToDB(OpenAISchema):
    "Save user transaction into database"
    amountOut: str
    amountIn: str
    currency: str
    sourceOrPayee: str
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
    ]
    description: str
    transactionDate: Annotated[str, Field(description="yyyymmdd")]


async def save_transaction_to_db(input: SaveTransactionToDB, user_id: str):
    print("save_transaction_to_db", input.model_dump())
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
    print(db_transaction)
    return "saved to db"


TOOLS = {
    "SaveTransactionToDB": {"fn": save_transaction_to_db, "schema": SaveTransactionToDB}
}

openai_tools = []
for tool_name in TOOLS:
    tool_schema = TOOLS[tool_name]["schema"].openai_schema
    openai_tools.append({"type": "function", "function": tool_schema})
