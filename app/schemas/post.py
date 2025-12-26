from pydantic import BaseModel
from datetime import datetime
import uuid

class PostCreate(BaseModel):
    caption: str = ""

class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    caption: str
    url: str
    file_type: str
    file_name: str
    created_at: datetime
    is_owner: bool
    email: str
