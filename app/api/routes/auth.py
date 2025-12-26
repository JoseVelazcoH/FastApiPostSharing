from fastapi import APIRouter
from app.core.security import fastapi_users, auth_backend
from app.schemas.user import UserRead, UserCreate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/jwt",
    tags=["auth"]
)
