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
async def test_get_wallet_success():
    wid = uuid.uuid4()
    wallet = Wallet(wid, Decimal("100"))
    session = MockAsyncSession(wallet)
    app.dependency_overrides[get_db] = override_db(session)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/wallets/{wid}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(wid)
    assert data["balance"] == "100"


@pytest.mark.asyncio
async def test_get_wallet_404():
    wid = uuid.uuid4()
    session = MockAsyncSession()
    app.dependency_overrides[get_db] = override_db(session)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/wallets/{wid}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Wallet not found"
