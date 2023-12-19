import datetime
import json
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
    print("db_transaction", db_transaction)
    return db_transaction.model_dump_json()


class QueryUserTransaction(OpenAISchema):
    "Query user transaction data from database"
    startDate: Annotated[str, Field(description="query startdate in yyyymmdd format")]
    endDate: Annotated[str, Field(description="query enddate in yyyymmdd format")]
    # sourceOrPayee: Annotated[str, Field(description="query sourceOrPayee column")] = None
    # category: Annotated[
    #     Literal[
    #         "Grocery",
    #         "FoodAndDining",
    #         "RentAndMortgage",
    #         "Utilities",
    #         "Transportation",
    #         "Entertainment",
    #         "Healthcare",
    #         "Clothing",
    #         "Education",
    #         "Miscellaneous",
    #     ],
    #     Field(description="query by category"),
    # ]
    # description: Annotated[str, Field(description="query by description")] = None
    # currency: Annotated[str, Field(description="query by currency")] = None


async def query_user_transaction(input: QueryUserTransaction, user_id: str):
    print("query_user_transaction",input)
    from libs.prisma import db

    # query data from db
    db_transactions = db.transaction.find_many(
        where={
            "userId": user_id,
            "transactionDate": {
                "gte": input.startDate if input.startDate else "00000000",
                "lte": input.endDate if input.endDate else "99991231",
            },
        },
    )
    
    filtered_transactions = []
    count = 0
    total_expense = 0
    expense_count = 0
    total_income = 0
    income_count = 0
    max_expense = 0
    min_expense = 0
    max_income = 0
    min_income = 0
    average_expense = 0
    average_income = 0
    for transaction in db_transactions:
        # # filter transaction
        # if input.sourceOrPayee and input.sourceOrPayee != transaction.sourceOrPayee:
        #     continue
        # if input.category and input.category != transaction.category:
        #     continue
        # if input.description and transaction.description.find(input.description) == -1:
        #     continue
        # if input.currency and input.currency != transaction.currency:
        #     continue
        transaction.createdAt = transaction.createdAt.strftime("%Y%m%d")
        transaction.updatedAt = transaction.updatedAt.strftime("%Y%m%d")
        
        # add transaction data
        transaction_data = transaction.model_dump()
        filtered_transactions.append(transaction_data)

        # record additional metrics
        amountIn = float(transaction.amountIn if transaction.amountIn else 0)
        amountOut = float(transaction.amountOut if transaction.amountOut else 0)

        count += 1
        total_expense += amountOut
        total_income += amountIn
        if amountOut > max_expense:
            max_expense = amountOut
        if amountOut < min_expense:
            min_expense = amountOut
        if amountIn > max_income:
            max_income = amountIn
        if amountIn < min_income:
            min_income = amountIn

    # calculate average expense and income
    average_expense = (total_expense / expense_count) if expense_count > 0 else 0
    average_income = (total_income / income_count) if income_count > 0 else 0

    report = {
        "transaction_count": count,
        "expense_count": expense_count,
        "income_count": income_count,
        "total_expense": total_expense,
        "total_income": total_income,
        "average_expense": average_expense,
        "average_income": average_income,
        "max_expense": max_expense,
        "min_expense": min_expense,
        "max_income": max_income,
        "min_income": min_income,
        "transaction_data": filtered_transactions,
    }

    print(report)
    return json.dumps(report)


# class QueryUserTransaction(OpenAISchema):
#     "To query user transaction data"
#     query: Annotated[str, Field(description="what to query")] = None

# async def query_user_transaction(input: QueryUserTransaction, user_id: str):
#     SYSTEM_PROMPT = """
#     userId is {user_id}
#     transaction date is written in yyyymmdd format

#     Given the following SQL tables, your job is to write queries given a user’s request.

    # CREATE TABLE "Transaction" (
    #     "id" TEXT NOT NULL,
    #     "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #     "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #     "amountOut" TEXT,
    #     "amountIn" TEXT,
    #     "currency" TEXT,
    #     "sourceOrPayee" TEXT,
    #     "category" "Category" NOT NULL DEFAULT 'Miscellaneous',
    #     "description" TEXT,
    #     "transactionDate" TEXT,
    #     "userId" TEXT,

    #     CONSTRAINT "Transaction_pkey" PRIMARY KEY ("id")
    # );

#     example query:
#     SELECT * FROM "Transaction"
#     """
#     from libs.genai import genai

#     genai.GenerativeModel("models/gemini-pro")
#     result = genai.generate_text(prompt=SYSTEM_PROMPT)

#     raise "Error"


TOOLS = {
    "SaveTransactionToDB": {
        "fn": save_transaction_to_db,
        "schema": SaveTransactionToDB,
    },
    "QueryUserTransaction": {
        "fn": query_user_transaction,
        "schema": QueryUserTransaction,
    },
}

openai_tools = []
for tool_name in TOOLS:
    tool_schema = TOOLS[tool_name]["schema"].openai_schema
    openai_tools.append({"type": "function", "function": tool_schema})
