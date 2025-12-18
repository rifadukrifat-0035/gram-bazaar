import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# 1. URL RETRIEVAL & FIX
# Render provides 'postgres://', but SQLAlchemy Async needs 'postgresql+asyncpg://'
raw_db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://gram_user:gram_password@db:5432/gram_bazaar")

if raw_db_url.startswith("postgres://"):
    DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = raw_db_url

# 2. ADVANCED ENGINE CONFIGURATION
# We use 'pool_pre_ping=True' to handle cloud database disconnects automatically.
# We increase 'pool_size' to handle more concurrent users (Standard for Production).
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to False in production to keep logs clean
    future=True,
    pool_pre_ping=True, # Critical: Checks connection health before query
    pool_size=20,       # Optimized for concurrent traffic
    max_overflow=10
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_db_session() -> AsyncSession:
    """
    Dependency that provides a database session for each request.
    Includes proper cleanup to prevent memory leaks.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() # Force update for Render deployment fix