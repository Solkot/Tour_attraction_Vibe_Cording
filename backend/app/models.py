from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TourLocation(Base):
    __tablename__ = "tour_locations"

    id = Column(Integer, primary_key=True, index=True)
    contentid = Column(String, unique=True, index=True, nullable=False) # 콘텐츠 고유 ID
    contenttypeid = Column(String, nullable=False)                      # 콘텐츠 유형 ID
    title = Column(String, nullable=False)                             # 장소명
    addr1 = Column(String, nullable=True)                              # 주소
    addr2 = Column(String, nullable=True)                              # 상세 주소
    zipcode = Column(String, nullable=True)                            # 우편번호
    tel = Column(String, nullable=True)                                # 전화번호
    mapx = Column(Float, nullable=True)                                # 경도 (WGS84, float 변환 저장)
    mapy = Column(Float, nullable=True)                                # 위도 (WGS84, float 변환 저장)
    cat1 = Column(String, nullable=True)                               # 대분류
    cat2 = Column(String, nullable=True)                               # 중분류
    cat3 = Column(String, nullable=True)                               # 소분류
    firstimage = Column(String, nullable=True)                         # 대표 이미지 URL

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    views = Column(Integer, nullable=False, server_default="0")
    
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="comments")