from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import TourLocation
from app.constants import REGION_DATA, CONTENT_TYPE_MAP
from app.schemas.tour import TourLocationResponse

def get_places_by_region(db: Session, region: str):
    target_regions = [region]
    if region in REGION_DATA:
        target_regions.extend(REGION_DATA[region])
    
    # 주소(addr1) 필드에 지역명이 포함되어 있는지 검사
    filters = [TourLocation.addr1.like(f"%{r}%") for r in target_regions]
    locations = db.query(TourLocation).filter(or_(*filters)).all()
    
    result = []
    for loc in locations:
        matched_region = region
        for r in target_regions:
            if r in (loc.addr1 or ""):
                matched_region = r
                break
                
        category_name = CONTENT_TYPE_MAP.get(loc.contenttypeid, "기타")
        
        result.append(
            TourLocationResponse(
                id=loc.id,
                contentid=loc.contentid,
                name=loc.title,
                category=category_name,
                region=matched_region,
                desc=loc.addr1,
                lat=loc.mapy,  
                lng=loc.mapx,       
                image=loc.firstimage
            )
        )
    return result