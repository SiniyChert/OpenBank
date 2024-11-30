from fastapi import APIRouter
import dbRequests as dbr
from schemas import TransactionSchema, Transaction, CurrencyPD

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("")
async def postTransaction(
    sender: str, recipient: str, sum: CurrencyPD, forced: bool = False
) -> TransactionSchema:
    pass


@router.get("")
async def getTransactionsPage(username: str, i: int) -> list[TransactionSchema]:
    pass
