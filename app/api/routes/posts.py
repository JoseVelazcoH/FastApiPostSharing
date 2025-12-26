from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.db.models import User, Post
from app.services import post_service

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    return await post_service.create_post(file, caption, user, session)

@router.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    posts = await post_service.get_all_posts(session, user)
    return {"posts": posts}

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await post_service.delete_post_by_id(post_id, user, session)
