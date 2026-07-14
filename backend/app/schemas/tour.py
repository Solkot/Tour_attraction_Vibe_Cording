from pydantic import BaseModel, ConfigDict
from typing import Optional

class TourLocationResponse(BaseModel):
    id: int
    contentid: str
    name: str
    category: str
    region: str
    desc: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    image: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)