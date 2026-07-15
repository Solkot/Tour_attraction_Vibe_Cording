from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Post
from app.schemas.post import (
    DeleteRequest,
    PostCreate,
    PostUpdate,
)


def create_post(db: Session, post_data: PostCreate):
    post = Post(
        title=post_data.title,
        content=post_data.content,
        category=post_data.category,
        password=post_data.password,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def get_posts(db: Session, category: Optional[str] = None):
    query = db.query(Post)

    if category:
        query = query.filter(Post.category == category)

    return query.order_by(Post.created_at.desc()).all()


def get_post(db: Session, post_id: int):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다.")

    # Increase view count
    try:
        post.views = (post.views or 0) + 1
        db.commit()
        db.refresh(post)
    except Exception:
        db.rollback()

    return post


def update_post(db: Session, post_id: int, post_data: PostUpdate):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다.")

    if post.password != post_data.password:
        raise HTTPException(401, "비밀번호가 일치하지 않습니다.")

    post.title = post_data.title
    post.content = post_data.content
    post.category = post_data.category

    db.commit()
    db.refresh(post)

    return post


def delete_post(db: Session, post_id: int, req: DeleteRequest):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다.")

    if post.password != req.password:
        raise HTTPException(401, "비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()

    return {"message": "게시글이 성공적으로 삭제되었습니다."}