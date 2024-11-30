from datetime import datetime


class Currency(int):
    """
    Валюта. Целое число, можно изменить
    """

    pass


class Entry:
    def __str__(self):
        return str(self.__dict__)


class User(Entry):
    def __init__(
        self,
        id: int,
        username: str,
        FIO: str,
        balance: Currency,
        isBanned: bool,
        isOrg: bool,
    ):
        self.id = id
        self.username = username
        self.FIO = FIO
        self.balance = balance
        self.isBanned = isBanned
        self.isOrg = isOrg


class Transaction(Entry):
    def __init__(
        self,
        Id: int,
        fromId: int,
        toId: int,
        datetime: datetime,
        sum: Currency,
    ):
        self.Id = Id
        self.fromId = fromId
        self.toId = toId
        self.datetime = datetime
        self.sum = sum


class TaxPayment(Entry):
    def __init__(self, Id: int, userId: int, taxId: int):
        self.Id = Id
        self.userId = userId
        self.taxId = taxId


class Tax(Entry):
    def __init__(self, Id: int, name: str, datetime: datetime, sum: Currency):
        self.Id = Id
        self.name = name
        self.datetime = datetime
        self.sum = sum


class CreditRequest(Entry):
    """
    Статус кредитной заявки
    1 - отправлена
    2 - рассматривается
    3 - одобрена
    4 - отклонена
    """

    def __init__(
        self,
        Id: int,
        userId: int,
        purpose: str,
        sum: Currency,
        status: int,
    ):
        self.Id = Id
        self.userId = userId
        self.purpose = purpose
        self.sum = sum
        self.status = status
