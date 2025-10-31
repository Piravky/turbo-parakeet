from decimal import Decimal

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import get_wallet_by_id, update_wallet_balance


async def deposit(wallet_uuid: UUID4, amount: Decimal, db: AsyncSession):
    wallet = await get_wallet_by_id(wallet_uuid, db)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    result_balance = wallet.balance + amount
    return await update_wallet_balance(wallet_uuid, result_balance, db)


async def withdraw(wallet_uuid: UUID4, amount: Decimal, db: AsyncSession):
    wallet = await get_wallet_by_id(wallet_uuid, db)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    result_balance = wallet.balance - amount
    if result_balance < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    return await update_wallet_balance(wallet_uuid, result_balance, db)
