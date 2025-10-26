from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
)

session_factory = async_sessionmaker(engine)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with session_factory() as session:
        yield session
