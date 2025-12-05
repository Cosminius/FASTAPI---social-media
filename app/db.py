from collections.abc import AsyncGenerator
from datetime import datetime
import uuid
from fastapi.params import Depends
from fastapi_users import UUIDIDMixin
from sqlalchemy import UUID, Column, ForeignKey, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

Base = declarative_base()

class User(Base, SQLAlchemyBaseUserTableUUID):
    posts=relationship("Post", back_populates="owner")



class Post(Base):
    __tablename__ = "posts"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"),  nullable=False)
    caption = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="posts")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)