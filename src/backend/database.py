# src/backend/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.core.config import get_settings

Base = declarative_base()
settings = get_settings()

# PostgreSQL with asyncpg
engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()