from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Comment, Post
from app.schemas.comment import CommentCreate
from app.schemas.post import DeleteRequest

def create_comment(db: Session, post_id: int, comment_data: CommentCreate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다.")

    comment = Comment(
        post_id=post_id,
        author=comment_data.author,
        content=comment_data.content,
        password=comment_data.password,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()

def delete_comment(db: Session, comment_id: int, req: DeleteRequest):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(404, "댓글을 찾을 수 없습니다.")
    if comment.password != req.password:
        raise HTTPException(401, "비밀번호가 일치하지 않습니다.")
    
    db.delete(comment)
    db.commit()
    return {"message": "댓글이 성공적으로 삭제되었습니다."}