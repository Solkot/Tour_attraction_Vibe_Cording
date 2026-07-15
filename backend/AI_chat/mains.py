# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from crud import get_nearby_spots
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try: yield db
#     finally: db.close()

# @app.post("/api/chat")
# async def chat(user_lat: float, user_lon: float, user_query: str, db: Session = Depends(get_db)):
#     # 1. DB에서 근처 관광지 검색
#     spots = get_nearby_spots(db, user_lat, user_lon)
    
#     # 2. 검색된 데이터를 문자열로 변환
#     context = "\n".join([f"- {s.title} ({s.addr1})" for s in spots])
    
#     # 3. OpenAI 호출
#     prompt = f"""
#     당신은 지역 여행 전문가입니다. 아래 참고 정보를 바탕으로 사용자의 질문에 답하세요.
#     참고 정보:
#     {context}
    
#     사용자 질문: {user_query}
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )
    
#     return {"reply": response.choices[0].message.content, "spots": spots}