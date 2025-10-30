# Python
from decimal import Decimal


class Wallet:
    def __init__(self, id_, balance: Decimal):
        self.id = id_
        self.balance = balance


class _ResultStub:
    def __init__(self, value):
        self._value = value

    def scalars(self):
        return self

    def first(self):
        return self._value


class MockAsyncSession:
    def __init__(self, wallet: Wallet | None = None):
        self.wallet = wallet
        self.committed = False
        self.refreshed = False

    async def execute(self, _query):
        return _ResultStub(self.wallet)

    async def commit(self):
        self.committed = True

    async def refresh(self, _obj):
        self.refreshed = True


def override_db(session: MockAsyncSession):
    async def _dep():
        yield session

    return _dep
