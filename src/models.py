import uuid

from sqlalchemy import (
    Column,
    UUID,
    Numeric,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    wallets = relationship("Wallet", back_populates="user")


class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric, nullable=False, default=0.0)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="wallets")
