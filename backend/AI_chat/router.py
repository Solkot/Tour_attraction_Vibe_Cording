import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from backend.database import get_db
from backend.AI_chat.crud import get_nearby_spots

# [배포 친화적 설정]
# 현재 파일(router.py) 위치에서 3단계 위로 올라가면 프로젝트 루트(maptest)가 나옵니다.
# 어디서 실행하든 항상 정확한 위치의 .env 파일을 찾습니다.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / '.env'

# .env 로드
load_dotenv(dotenv_path=ENV_PATH)

# API 키 가져오기
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # 에러를 명확하게 하여 디버깅을 돕습니다.
    raise ValueError(f"🚨 .env 파일에서 GEMINI_API_KEY를 찾을 수 없습니다! 경로 확인: {ENV_PATH}")

genai.configure(api_key=api_key)

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
        
        # 2. Gemini 모델 설정 (현재 사용 가능한 모델명으로 지정)
        model = genai.GenerativeModel('models/gemini-3.5-flash')
        prompt = f"사용자 질문: {request.user_query}\n근처 관광지:\n{spots_context}\n답변해줘."
        
        # 3. AI 답변 생성
        response = model.generate_content(prompt)
        return {"reply": response.text}
        
    except Exception as e:
        print(f"🚨 에러 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))