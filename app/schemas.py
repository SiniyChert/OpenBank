from typing import Any
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from datetime import datetime
from classes import User, Transaction, Currency, CreditRequest, Tax, TaxPayment


class CurrencyPD(Currency):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(int))
# я не понимаю как, но это работает. если надо поменять базовый тип Currency, надо изменить handler в 13 строчке на нужный тип

class UserSchema(BaseModel, arbitrary_types_allowed=True):
    id: int
    username: str
    FIO: str
    balance: CurrencyPD
    isBanned: bool
    isOrg: bool

    def to_user(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            FIO=self.FIO,
            balance=self.balance,
            isBanned=self.isBanned,
            isOrg=self.isOrg,
        )

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            FIO=user.FIO,
            balance=user.balance,
            isBanned=user.isBanned,
            isOrg=user.isOrg,
        )


class TransactionSchema(BaseModel, arbitrary_types_allowed=True):
    Id: int
    fromId: int
    toId: int
    datetime: datetime
    sum: CurrencyPD

    def to_transaction(self) -> Transaction:
        return Transaction(
            Id=self.Id,
            fromId=self.fromId,
            toId=self.toId,
            datetime=self.datetime,
            sum=self.sum,
        )

    @classmethod
    def from_transaction(cls, transaction: Transaction):
        return cls(
            Id=transaction.Id,
            fromId=transaction.fromId,
            toId=transaction.toId,
            datetime=transaction.datetime,
            sum=transaction.sum,
        )


class TaxPaymentSchema(BaseModel):
    Id: int
    userId: int
    taxId: int

    def to_tax_payment(self) -> TaxPayment:
        return TaxPayment(Id=self.Id, userId=self.userId, taxId=self.taxId)

    @classmethod
    def from_tax_payment(cls, tax_payment: TaxPayment):
        return cls(
            Id=tax_payment.Id, userId=tax_payment.userId, taxId=tax_payment.taxId
        )


class TaxSchema(BaseModel):
    Id: int
    sum: CurrencyPD
    datetime: datetime
    name: str

    def to_tax(self) -> Tax:
        return Tax(Id=self.Id, name=self.name, datetime=self.datetime, sum=self.sum)

    @classmethod
    def from_tax(cls, tax: Tax):
        return cls(Id=tax.Id, name=tax.name, datetime=tax.datetime, sum=tax.sum)


class CreditRequestSchema(BaseModel):
    Id: int
    userId: int
    purpose: str
    sum: CurrencyPD
    status: int

    def to_credit_request(self) -> CreditRequest:
        return CreditRequest(
            Id=self.Id,
            userId=self.userId,
            purpose=self.purpose,
            sum=self.sum,
            status=self.status,
        )

    @classmethod
    def from_credit_request(cls, credit_request: CreditRequest):
        return cls(
            Id=credit_request.Id,
            userId=credit_request.userId,
            purpose=credit_request.purpose,
            sum=credit_request.sum,
            status=credit_request.status,
        )
