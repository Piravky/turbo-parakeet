from decimal import Decimal

from pydantic import BaseModel, UUID4, field_validator


class WalletPublic(BaseModel):
    id: UUID4
    balance: Decimal


class WalletOperations(BaseModel):
    operation_type: str
    amount: Decimal

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("The amount must be positive!")
        return v
