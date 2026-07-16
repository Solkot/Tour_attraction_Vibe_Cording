import json
import os
import sys

# 모듈 경로 문제 해결
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal, engine, Base
from app.models import TourLocation

# 1. 적재할 파일 목록
DATA_FILES = [
    "구미_경북권_관광지.json",
    "구미_경북권_레포츠.json",
    "구미_경북권_문화시설.json",
    "구미_경북권_쇼핑.json",
    "구미_경북권_숙박.json",
    "구미_경북권_여행코스.json",
    "구미_경북권_음식점.json",
    "구미_경북권_축제공연행사.json"
]

def seed_data():
    db = SessionLocal()
    data_dir = os.path.join(os.path.dirname(__file__), "../../data")
    
    # 이미 데이터가 있는지 확인 (전체 테이블 기준)
    if db.query(TourLocation).first():
        print("이미 데이터가 DB에 존재합니다. 세딩을 건너뜁니다.")
        db.close()
        return

    total_loaded = 0
    
    for filename in DATA_FILES:
        json_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(json_path):
            print(f"경고: {filename} 파일을 찾을 수 없습니다. 건너뜁니다.")
            continue
            
        print(f"{filename} 파싱 중...")
        
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        # 데이터 구조 확인 (items가 리스트인지 확인)
        items = raw_data.get("items", []) if isinstance(raw_data, dict) else raw_data
        
        for item in items:
            content_id = item.get("contentid")
            if not content_id:
                continue
            if item.get("addr1") and item.get("addr1").startswith("대구"):
                continue
            
            # mapx, mapy 실수 변환
            mapx_val = item.get("mapx")
            mapy_val = item.get("mapy")
            
            location = TourLocation(
                contentid=str(content_id), # 혹시 모를 타입 불일치 방지
                contenttypeid=str(item.get("contenttypeid")),
                title=item.get("title"),
                addr1=item.get("addr1"),
                addr2=item.get("addr2"),
                zipcode=item.get("zipcode"),
                tel=item.get("tel"),
                mapx=float(mapx_val) if mapx_val and str(mapx_val).strip() else None,
                mapy=float(mapy_val) if mapy_val and str(mapy_val).strip() else None,
                cat1=item.get("cat1"),
                cat2=item.get("cat2"),
                cat3=item.get("cat3"),
                firstimage=item.get("firstimage")
            )
            db.add(location)
            total_loaded += 1

    try:
        db.commit()
        print(f"\n총 {total_loaded}건의 데이터를 SQLite DB에 적재 완료했습니다!")
    except Exception as e:
        db.rollback()
        print(f"DB 적재 실패: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()