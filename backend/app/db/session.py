# backend/app/db/session.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# In a real app, get this from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://gram_user:gram_password@db:5432/gram_bazaar")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_db_session() -> AsyncSession:
    """Dependency that provides a database session for each request."""
    async with async_session() as session:
        yield session
