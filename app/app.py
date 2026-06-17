from fastapi import FastAPI ,HTTPException ,File , UploadFile, Depends,Form
from app.schema import PostCreate , PostResponse
from app.db import Post , create_db_and_tables , get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield



app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    caption:str=Form(...),
    session:AsyncSession=Depends(get_async_session)  #dependency injection
):
    post=Post(
        caption=caption,
        url="dummyurl",
        file_type="photo",
        file_name="dummyfilename"
    )
    session.add(post)
    await session.commit()  #adds the data to model
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(
    session:AsyncSession=Depends(get_async_session)
):
    result= await session.execute(select(Post).order_by(Post.created_At.desc()))
    posts= [row[0] for row in result.all()]
    