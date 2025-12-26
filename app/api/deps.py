from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_async_session
from app.db.models import User
from app.core.security import current_active_user

async def get_db():
    async for session in get_async_session():
        yield session

async def get_current_user(user: User = Depends(current_active_user)) -> User:
    return user
