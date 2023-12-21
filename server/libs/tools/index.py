import datetime
import json
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from instructor import OpenAISchema
from dotenv import load_dotenv
import os

load_dotenv()


class SaveTransactionToDB(OpenAISchema):
    "To save user transaction after user confirmed the correctness of transaction data"
    amountOut: Annotated[str, Field(description="expense amount example: 25.78")] = "0"
    amountIn: Annotated[str, Field(description="income amount example: 500.00")] = "0"
    currency: Annotated[str, Field(description="currency symbol, example: USD, PHP, EUR, GBP")] = "0"
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
    transactionDate: Annotated[str, Field(description="yyyymmdd")]


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
    "Query user transaction data"
    startDate: Annotated[
        str, Field(description="query startdate in yyyymmdd format")
    ] = "00000101"
    endDate: Annotated[
        str, Field(description="query enddate in yyyymmdd format")
    ] = "99991231"
    queryKeywords: Annotated[
        str, Field(description="query keywords related to transaction")
    ] = "I want all transaction data"
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
    print("query_user_transaction", input)
    from libs.prisma import db

    # query data from db
    db_transactions = db.transaction.find_many(
        where={
            "userId": user_id,
            "transactionDate": {
                "gte": input.startDate,
                "lte": input.endDate,
            },
        },
    )
    # from deps.openai import openai
    # class Response(BaseModel):
    #     is_within_query: Annotated[bool,Field(description="True if the transaction is within the query else False")]

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
        # filter transactions
        # call llm to filter transaction by query
        # res :Response = await openai.chat.completions.create(
        #     model="gpt-3.5-turbo-1106",
        #     response_model=Response,
        #     messages=[
        #         {
        #             "role":"system",
        #             "content":"Given a transaction data and a query, return True if transaction is within the query else False"
        #         },
        #         {
        #             "role":"user",
        #             "content":json.dumps(transaction.model_dump_json())
        #         }
        #     ]
        # )

        # if not res.is_within_query:
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
    # we use gemini to filter transactions
    from deps.llamaindex import GeminiPro
    from llama_index.llms import ChatMessage, MessageRole, ChatResponse

    res = await GeminiPro.achat(
        messages=[
            ChatMessage(
                role=MessageRole.USER,
                content=f"""Given these transactions data, answer this query: {input.queryKeywords}
                
                transactions data:
                
                {json.dumps(report)}
                """,
            )
        ]
    )
    return res.message.content


class ReadUserTransactionChart(OpenAISchema):
    "Create a chart of user transaction"
    startDate: Annotated[str, Field(description="query startdate in yyyymmdd format")] = "00000101"
    endDate: Annotated[str, Field(description="query enddate in yyyymmdd format")] = "99991231"


async def read_user_transaction_chart(input: ReadUserTransactionChart, user_id: str):
    CLIENT_BASE_URL = os.getenv("CLIENT_BASE_URL")

    return f"{CLIENT_BASE_URL}/dashboard/user_id/{user_id}/start_date/{input.startDate}/end_date/{input.endDate}"


TOOLS = {
    "SaveTransactionToDB": {
        "fn": save_transaction_to_db,
        "schema": SaveTransactionToDB,
    },
    "QueryUserTransaction": {
        "fn": query_user_transaction,
        "schema": QueryUserTransaction,
    },
    "ReadUserTransactionChart": {
        "fn": read_user_transaction_chart,
        "schema": ReadUserTransactionChart,
    },
}

openai_tools = []
for tool_name in TOOLS:
    tool_schema = TOOLS[tool_name]["schema"].openai_schema
    openai_tools.append({"type": "function", "function": tool_schema})
