from fastapi import APIRouter
import dbRequests as dbr
from schemas import CreditRequestSchema, CurrencyPD

router = APIRouter(prefix="/credits", tags=["credits"])


@router.get("")
async def getCreditRequests() -> list[CreditRequestSchema]:
    return [CreditRequestSchema.from_credit_request(i) for i in dbr.getCreditRequests()]


@router.post("")
async def postCreditRequest(
    userId: int,
    purpose: str,
    sum: CurrencyPD,
    status: int = 1,
) -> CreditRequestSchema | None:
    res = dbr.postCreditRequest(userId, purpose, sum, status)
    if res is not None:
        return CreditRequestSchema.from_credit_request(res)
    return None


@router.get("/{id}")
async def getCreditRequest(id: int) -> CreditRequestSchema | None:
    res = dbr.getCreditRequest(id)
    if res is not None:
        return CreditRequestSchema.from_credit_request(res)
    return None


@router.put("/{id}")
async def setCreditRequestStatus(id: int, newStatus: int) -> CreditRequestSchema | None:
    res = dbr.setCreditRequestStatus(id, newStatus)
    if res is not None:
        return CreditRequestSchema.from_credit_request(res)
    return None
