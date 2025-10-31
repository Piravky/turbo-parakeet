from decimal import Decimal

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Wallet


async def get_wallet_by_id(wallet_uuid: UUID4, db: AsyncSession):
    result = await db.execute(select(Wallet).filter(Wallet.id == wallet_uuid))
    return result.scalars().first()


async def update_wallet_balance(wallet_uuid: UUID4, new_balance: Decimal, db: AsyncSession):
    wallet = await get_wallet_by_id(wallet_uuid, db)
    setattr(wallet, 'balance', new_balance)
    await db.commit()
    await db.refresh(wallet)
    return wallet
