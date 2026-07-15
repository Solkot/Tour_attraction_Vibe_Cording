from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Spot(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, index=True)
    contentid = Column(String, unique=True)
    title = Column(String)
    addr1 = Column(String)
    mapx = Column(Float)
    mapy = Column(Float)
    firstimage = Column(String)