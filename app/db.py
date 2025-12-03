from collections.abc import AsyncGenerator
from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship


DATABASE_URL = "sqlite+aiosqlite:///./test.db"

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)
    file_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session