from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comment import CommentCreate, CommentResponse
from app.schemas.post import DeleteRequest
from app.services import comment_service

router = APIRouter(
    prefix="/api/posts/{post_id}/comments",
    tags=["Comments"],
)

@router.post(
    "",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
):
    return comment_service.create_comment(db, post_id, comment_data)

@router.get(
    "",
    response_model=List[CommentResponse],
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    return comment_service.get_comments(db, post_id)

@router.delete("/{comment_id}")
def delete_comment(
    post_id: int,
    comment_id: int,
    password: str = Query(...),
    db: Session = Depends(get_db),
):
    req = DeleteRequest(password=password)
    return comment_service.delete_comment(db, comment_id, req)