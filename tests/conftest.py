import sys
import os
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure `backend` is on sys.path so `import app` works
ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.database import Base


@pytest.fixture(scope="session")
def tmp_db_path(tmp_path_factory):
    p = tmp_path_factory.mktemp("data") / "test.db"
    return p


@pytest.fixture(scope="session")
def engine(tmp_db_path):
    url = f"sqlite:///{tmp_db_path}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(engine, monkeypatch):
    from fastapi.testclient import TestClient

    # import app AFTER sys.path modified
    import app.main as app_main
    import app.database as app_database

    # override get_db to use test engine
    def override_get_db():
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app_main.app.dependency_overrides[app_database.get_db] = override_get_db

    client = TestClient(app_main.app)
    yield client
