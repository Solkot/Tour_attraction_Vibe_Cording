from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.post import router as post_router
from app.routers.comment import router as comment_router
from app.routers.tour import router as tour_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyGumi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(comment_router)
app.include_router(tour_router)