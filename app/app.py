from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from sqlalchemy import select
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import tempfile
from app.images import imagekit_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/upload/")
async def upload_post(
    file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as f:
            upload_result = imagekit_client.upload_file(
                file=f,
                file_name=file.filename,
                options=UploadFileRequestOptions(
                    use_unique_file_name=True,
                    tags=["backend-upload"]
                )
            )

        url = getattr(upload_result, "url", None)
        if not url:
            raise HTTPException(status_code=500, detail="ImageKit upload failed: no URL returned")

        post = Post(
            caption=caption,
            url=url,
            file_type="video" if file.content_type and file.content_type.startswith("video/") else "image",
            file_name=file.filename
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": post.id,
                "caption": post.caption,
                "url": post.url,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat() if post.created_at else None
            }
        )
    return {"posts": posts_data}