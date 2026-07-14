from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.database import SessionLocal, engine, Base
from app.models import Post, Comment

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyGumi API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 세션 의존성 Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic 스키마 (데이터 검증용) ---
class PostCreate(BaseModel):
    title: str
    content: str
    category: str
    password: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True

class DeleteRequest(BaseModel):
    password: str


# --- API 엔드포인트 구현 ---

# 1. 게시글 작성
@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        category=post_data.category,
        password=post_data.password  # 단순 평문 저장 (요구사항 기준)
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 2. 게시글 목록 조회
@app.get("/api/posts", response_model=List[PostResponse])
def get_posts(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Post)
    if category:
        query = query.filter(Post.category == category)
    # 최신순 정렬
    return query.order_by(Post.created_at.desc()).all()

# 3. 게시글 상세 조회
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post

# 4. 게시글 삭제 (비밀번호 확인)
@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, req: DeleteRequest, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    if post.password != req.password:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
        
    db.delete(post)
    db.commit()
    return {"message": "게시글이 성공적으로 삭제되었습니다."}