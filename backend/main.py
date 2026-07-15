import os
import json
from fastapi import FastAPI
from backend.database import engine, Base, SessionLocal
from backend.AI_chat.models import Spot
from backend.AI_chat.router import router as chat_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 도메인 허용 (개발용)
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    # 1. 모든 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 2. 데이터 초기화 (필요시)
    db = SessionLocal()
    try:
        if db.query(Spot).first() is None:
            json_path = os.path.join(os.path.dirname(__file__), "../data/spots.json")
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                items = data.get("items", [])
                spots = [Spot(
                    contentid=item['contentid'],
                    title=item['title'],
                    addr1=item['addr1'],
                    mapx=float(item['mapx']),
                    mapy=float(item['mapy']),
                    firstimage=item['firstimage']
                ) for item in items]
                db.bulk_save_objects(spots)
                db.commit()
            print("데이터 초기화 완료.")
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(chat_router)