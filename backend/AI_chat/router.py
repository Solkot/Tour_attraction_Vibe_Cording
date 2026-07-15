from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.AI_chat.crud import get_nearby_spots
import backend.services.ai_service
from backend.services.ai_service import get_ai_response


router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    user_query: str
    lat: float
    lon: float

@router.post("/chat")
async def chat_with_bot(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 1. 주변 관광지 정보 조회
        spots = get_nearby_spots(db, request.lat, request.lon)
        spots_context = "\n".join([f"- {s.title} (주소: {s.addr1})" for s in spots])
        
        # 2. AI 서비스 호출 (모델이 무엇인지는 신경 안 써도 됨!)
        answer = get_ai_response(request.user_query, spots_context)
        
        return {"reply": answer}
        
    except Exception as e:
        print(f"🚨 에러 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))