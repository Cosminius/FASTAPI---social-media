from collections.abc import AsyncGenerator
from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Declarative_base, relationship

DATABASE_URL ="sqlite+aiosqlite:///./test.db"

class Post(Declarative_base):
    __tablename__="posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    url = Column(String(200), nullable = False)
    file_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default = datetime.now())

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Declarative_base().metadata.create_all)


async def get_async_session()-> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session