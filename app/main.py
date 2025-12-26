from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import create_db_and_tables
from app.api.routes import auth, users, posts

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(posts.router, prefix="")
