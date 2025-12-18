import os
from typing import AsyncGenerator  # <--- NEW IMPORT ADDED
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# 1. URL RETRIEVAL & FIX
raw_db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://gram_user:gram_password@db:5432/gram_bazaar")

if raw_db_url.startswith("postgres://"):
    DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = raw_db_url

# 2. ADVANCED ENGINE CONFIGURATION
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# --- TYPE HINT FIX BELOW ---
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session for each request.
    Yields an AsyncSession and closes it after the request is done.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()