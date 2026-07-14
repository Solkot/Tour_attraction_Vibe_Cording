from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 프로젝트 폴더 내에 localhub.db 파일 생성 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./localhub.db"

engine = create_engine(
    # SQLite를 다중 스레드 환경(FastAPI)에서 안전하게 쓰기 위한 옵션
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()