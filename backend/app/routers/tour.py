from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.tour import TourLocationResponse
from app.services import tour_service

router = APIRouter(prefix="/api/places", tags=["places"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[TourLocationResponse])
def read_places(region: str = Query(..., description="행정구역명"), db: Session = Depends(get_db)):
    return tour_service.get_places_by_region(db, region)