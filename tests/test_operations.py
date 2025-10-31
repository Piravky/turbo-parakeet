import asyncio
import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient, ASGITransport

from src.database import get_db
from src.main import app
from tests.test_db import MockAsyncSession, Wallet, override_db


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_deposit_404():
    wid = uuid.uuid4()
    session = MockAsyncSession()
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "DEPOSIT", "amount": 100}
        )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Wallet not found"


@pytest.mark.asyncio
async def test_deposit_success():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "DEPOSIT", "amount": 100}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(wid)
    assert data["balance"] == "200"


@pytest.mark.asyncio
async def test_deposit_negative_amount():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "WITHDRAW", "amount": -1000}
        )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        e.get("loc") == ["body", "amount"]
        and "The amount must be positive!" in e.get("msg", "")
        for e in errors
    )


@pytest.mark.asyncio
async def test_deposit_concurrent_requests():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("0"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        async def do_deposit(amount: int | str):
            return await ac.post(
                f"/api/v1/wallets/{wid}/operations",
                json={"operation_type": "DEPOSIT", "amount": amount},
            )

        tasks = [do_deposit(10) for _ in range(10)]
        responses = await asyncio.gather(*tasks)

    assert all(r.status_code == 200 for r in responses)

    data = responses[-1].json()
    assert data["id"] == str(wid)
    assert data["balance"] == "100"


@pytest.mark.asyncio
async def test_withdraw_404():
    wid = uuid.uuid4()
    session = MockAsyncSession()
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "WITHDRAW", "amount": 100}
        )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Wallet not found"


@pytest.mark.asyncio
async def test_withdraw_success():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "WITHDRAW", "amount": 100}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(wid)
    assert data["balance"] == "0"


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "WITHDRAW", "amount": 1000}
        )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Insufficient funds"


@pytest.mark.asyncio
async def test_withdraw_concurrent_requests():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        async def do_deposit(amount: int | str):
            return await ac.post(
                f"/api/v1/wallets/{wid}/operations",
                json={"operation_type": "WITHDRAW", "amount": amount},
            )

        tasks = [do_deposit(10) for _ in range(10)]
        responses = await asyncio.gather(*tasks)

    assert all(r.status_code == 200 for r in responses)

    data = responses[-1].json()
    assert data["id"] == str(wid)
    assert data["balance"] == "0"


@pytest.mark.asyncio
async def test_withdraw_negative_amount():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "WITHDRAW", "amount": -1000}
        )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        e.get("loc") == ["body", "amount"]
        and "The amount must be positive!" in e.get("msg", "")
        for e in errors
    )


@pytest.mark.asyncio
async def test_wrong_operation():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with (AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac):
        response = await ac.post(
            f"/api/v1/wallets/{wid}/operations",
            json={"operation_type": "PLUS", "amount": 100}
        )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Operation type not supported"
