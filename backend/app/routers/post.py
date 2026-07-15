from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post import (
    DeleteRequest,
    PostCreate,
    PostResponse,
    PostUpdate,
)
from app.services import post_service

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"],
)


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
):
    return post_service.create_post(db, post_data)


@router.get(
    "",
    response_model=List[PostResponse],
)
def get_posts(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return post_service.get_posts(db, category)


@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    return post_service.get_post(db, post_id)


@router.put(
    "/{post_id}",
    response_model=PostResponse,
)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
):
    return post_service.update_post(
        db,
        post_id,
        post_data,
    )


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    password: str = Query(...),
    db: Session = Depends(get_db),
):
    req = DeleteRequest(password=password)
    return post_service.delete_post(
        db,
        post_id,
        req,
    )