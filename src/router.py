from fastapi import APIRouter, HTTPException, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import WalletPublic, WalletOperations
from src.crud import get_wallet_by_id
from src.database import get_db
from src.utils import deposit, withdraw

router = APIRouter(
    prefix="/wallets",
)


@router.post("/{wallet_uuid}/operations", name="Deposit/Withdraw operations", response_model=WalletPublic)
async def create_operation(wallet_uuid: UUID4, operation: WalletOperations, db: AsyncSession = Depends(get_db)):
    if operation.operation_type.upper() == "DEPOSIT":
        return await deposit(wallet_uuid, operation.amount, db)
    elif operation.operation_type.upper() == "WITHDRAW":
        return await withdraw(wallet_uuid, operation.amount, db)
    else:
        raise HTTPException(status_code=400, detail="Operation type not supported")


@router.get("/{wallet_uuid}", response_model=WalletPublic)
async def get_wallet(wallet_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    result = await get_wallet_by_id(wallet_uuid, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return result
