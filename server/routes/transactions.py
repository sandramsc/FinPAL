from typing import Annotated
from fastapi import APIRouter
from pydantic import BaseModel, Field
from prisma.models import Transaction


router = APIRouter(prefix="/transactions", tags=["transactions"])


class ReadTransactionsResponse(BaseModel):
    transactions: list[Transaction]


@router.get("/")
async def read_transactions(
    user_id: str,
    start_date: Annotated[str, Field(description="start_date in yyyymmdd format")],
    end_date: Annotated[str, Field(description="end_date in yyyymmdd format")],
) -> ReadTransactionsResponse:
    from libs.prisma import db

    res = db.transaction.find_many(
        where={
            "userId": user_id,
            "transactionDate": {"gte": start_date, "lte": end_date},
        }
    )

    return ReadTransactionsResponse(transactions=res)
