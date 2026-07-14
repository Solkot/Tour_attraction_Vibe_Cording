from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    content: str
    category: str
    password: str


class PostUpdate(BaseModel):
    title: str
    content: str
    category: str
    password: str


class DeleteRequest(BaseModel):
    password: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)