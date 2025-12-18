import os
from typing import AsyncGenerator  # <--- এই লাইনটি এরর ফিক্স করবে
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# 1. URL RETRIEVAL & FIX FOR RENDER
# Render 'postgres://' দেয়, কিন্তু SQLAlchemy 'postgresql+asyncpg://' চায়।
raw_db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://gram_user:gram_password@db:5432/gram_bazaar")

if raw_db_url.startswith("postgres://"):
    DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = raw_db_url

# 2. ADVANCED ENGINE CONFIGURATION (Production Ready)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,       # প্রোডাকশনে লগ বন্ধ রাখা ভালো
    future=True,
    pool_pre_ping=True, # কানেকশন ড্রপ করলে অটোমেটিক রিকানেক্ট করবে
    pool_size=20,       # একসাথে অনেক ইউজার হ্যান্ডেল করার ক্ষমতা
    max_overflow=10
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# 3. DATABASE DEPENDENCY WITH CORRECT TYPE HINT
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session for each request.
    Yields an AsyncSession and closes it ensuring no memory leaks.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()