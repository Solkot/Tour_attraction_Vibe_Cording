import json
import os
import sys

# 모듈 경로 문제 해결
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import TourLocation

# 이번에는 관광지 데이터 1개만 처리
DATA_FILE = "구미_경북권_관광지.json"

def seed_data():
    db = SessionLocal()
    
    # 중복 적재 방지
    if db.query(TourLocation).first():
        print("ℹ️ 이미 관광 데이터가 DB에 존재합니다. 세딩을 건너뜁니다.")
        db.close()
        return

    data_dir = os.path.join(os.path.dirname(__file__), "../../data")
    json_path = os.path.join(data_dir, DATA_FILE)
    
    if not os.path.exists(json_path):
        print(f"❌ 에러: {DATA_FILE} 파일이 data/ 폴더에 존재하지 않습니다.")
        db.close()
        return
        
    print(f"📦 {DATA_FILE} 파싱 중...")
    
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    items = raw_data.get("items", []) if isinstance(raw_data, dict) else raw_data
    
    loaded_count = 0
    for item in items:
        content_id = item.get("contentid")
        if not content_id:
            continue
            
        # mapx, mapy 실수 변환
        mapx_val = item.get("mapx")
        mapy_val = item.get("mapy")
        mapx = float(mapx_val) if mapx_val and str(mapx_val).strip() else None
        mapy = float(mapy_val) if mapy_val and str(mapy_val).strip() else None

        location = TourLocation(
            contentid=content_id,
            contenttypeid=item.get("contenttypeid"),
            title=item.get("title"),
            addr1=item.get("addr1") or None,
            addr2=item.get("addr2") or None,
            zipcode=item.get("zipcode") or None,
            tel=item.get("tel") or None,
            mapx=mapx,
            mapy=mapy,
            cat1=item.get("cat1") or None,
            cat2=item.get("cat2") or None,
            cat3=item.get("cat3") or None,
            firstimage=item.get("firstimage") or None
        )
        db.add(location)
        loaded_count += 1

    try:
        db.commit()
        print(f"\n🎉 성공적으로 {loaded_count}건의 관광지 데이터를 SQLite DB(localhub.db)에 적재 완료했습니다!")
    except Exception as e:
        db.rollback()
        print(f"❌ DB 적재 실패: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # 테이블 생성 후 실행
    Base.metadata.create_all(bind=engine)
    seed_data()