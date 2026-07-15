from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import Base, engine
from app.routers.chat import router as chat_router
from app.routers.comment import router as comment_router
from app.routers.post import router as post_router
from app.routers.tour import router as tour_router


# SQLAlchemy 모델을 기준으로 존재하지 않는 테이블을 생성한다.
# 기존 테이블과 데이터는 삭제하지 않는다.
Base.metadata.create_all(bind=engine)


# 기존 posts 테이블에 views 컬럼이 없을 때만 추가한다.
with engine.begin() as conn:
    try:
        columns = conn.execute(
            text("PRAGMA table_info('posts')")
        ).mappings().all()

        has_views_column = any(
            column.get("name") == "views"
            for column in columns
        )

        if not has_views_column:
            conn.execute(
                text(
                    "ALTER TABLE posts "
                    "ADD COLUMN views INTEGER DEFAULT 0"
                )
            )

    except Exception:
        # 컬럼 보정에 실패하더라도
        # 서버 전체 실행을 막지는 않도록 한다.
        pass


app = FastAPI(
    title="MyGumi API",
    description="구미 지역 관광·커뮤니티·AI 챗봇 API",
    version="1.0.0",
)


# 프론트엔드에서 백엔드 API에 접근할 수 있도록 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 기존 게시글 API
app.include_router(post_router)

# 기존 댓글 API
app.include_router(comment_router)

# 기존 관광지 API
app.include_router(tour_router)

# 새로 추가한 AI 챗봇 API
app.include_router(chat_router)


@app.get(
    "/",
    tags=["Health Check"],
    summary="서버 상태 확인",
)
def read_root():
    """
    백엔드 서버가 정상적으로 실행 중인지 확인한다.
    """

    return {
        "message": "서버가 정상적으로 작동 중입니다.",
    }