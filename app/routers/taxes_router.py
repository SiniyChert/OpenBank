from datetime import datetime
from fastapi import APIRouter
import dbRequests as dbr
from schemas import TaxSchema, TaxPaymentSchema, CurrencyPD, UserSchema

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.get("")
async def getTaxes() -> list[TaxSchema]:
    return [TaxSchema.from_tax(i) for i in dbr.getTaxes()]


@router.post("")
async def newTax(
    name: str = "", datetime: datetime = "2000-01-01 00:00:00", sum: CurrencyPD = 0
) -> TaxSchema | None:
    res = dbr.newTax(name, datetime, sum)
    if res is not None:
        return TaxSchema.from_tax(res)
    return None


@router.put("/{taxId}")
async def editTax(
    taxId: int, newName: str = None, newDateTime: datetime = None, newSum: int = None
) -> TaxSchema | None:
    res = dbr.editTax(taxId, newName, newDateTime, newSum)
    if res is not None:
        return TaxSchema.from_tax(res)
    return None


@router.post("/payments")
async def newTaxPayment(userId: int, taxId: int) -> TaxPaymentSchema | None:
    res = dbr.newTaxPayment(userId, taxId)
    if res is not None:
        return TaxPaymentSchema.from_tax_payment(res)
    return None


@router.get("/{taxId}")
async def getTax(taxId: int):
    res = dbr.getTax(taxId)
    if res is not None:
        return TaxSchema.from_tax(res)
    return None


@router.get("/{taxId}/stats")
async def getTaxStats(taxId: int):
    return dbr.getTaxStats(taxId)


@router.get("/{taxId}/defaulters")
async def getTaxDefaulters(taxId: int) -> list[UserSchema]:
    return [UserSchema.from_user(i) for i in dbr.getTaxDefaulters(taxId)]
