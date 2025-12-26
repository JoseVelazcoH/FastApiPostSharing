import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Post, User
from app.services.imagekit_service import upload_file_to_imagekit

async def create_post(file: UploadFile, caption: str, user: User, session: AsyncSession) -> Post:
    upload_data = await upload_file_to_imagekit(file)

    post = Post(
        user_id=user.id,
        caption=caption,
        url=upload_data["url"],
        file_type="video" if file.content_type.startswith("video/") else "image",
        file_name=upload_data["file_name"]
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def get_all_posts(session: AsyncSession, current_user: User) -> list[dict]:
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    users_dict = {user.id: user for user in users}

    post_data = []
    for post in posts:
        post_data.append({
            "id": str(post.id),
            "user_id": str(post.user_id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat(),
            "is_owner": post.user_id == current_user.id,
            "email": users_dict.get(post.user_id, User(email="unknown")).email
        })

    return post_data

async def delete_post_by_id(post_id: str, user: User, session: AsyncSession) -> dict:
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted succesfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
