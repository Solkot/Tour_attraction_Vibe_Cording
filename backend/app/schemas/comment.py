from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    author: str
    content: str
    password: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)