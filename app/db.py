#we need to keep a databse connection so that all posted entry can be saved

from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String , Text , DateTime ,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase , relationship 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine , async_sessionmaker
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts =relationship("Post",back_populates="user")
#define datamodels so our input data gets stored there

#inherit so we know we are making a model

#we created one to many reationship
class Post(Base):
     __tablename__="posts"
     
     id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
     user_id=Column(UUID(as_uuid=True),ForeignKey("user.id"),nullable=False)
     caption = Column(Text)
     url=Column(String,nullable=False)
     file_type= Column(String, nullable=False)
     file_name= Column(String, nullable=False)
     created_at=Column(DateTime,default=datetime.utcnow)
     
     user= relationship("User",back_populates="posts")
     
     
#we are making a databse engine that can look at this models and create a database for us

engine= create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#this finds everything form the declarative model and creates us a database for it
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)