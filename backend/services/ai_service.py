import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

# .env 로드
load_dotenv()

# 환경 변수로 모델 선택 (기본값: gemini)
# 나중에 OpenAI로 바꾸려면 이 값을 'openai'로 변경하면 됩니다.
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

def get_ai_response(user_query: str, spots_context: str) -> str:
    prompt = f"사용자 질문: {user_query}\n근처 관광지:\n{spots_context}\n답변해줘."

    if AI_PROVIDER == "gemini":
        return _call_gemini(prompt)
    elif AI_PROVIDER == "openai":
        return _call_openai(prompt)
    else:
        return "지원하지 않는 AI 제공자입니다."

def _call_gemini(prompt: str) -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-3.5-flash') # 모델명 확인 필요
    response = model.generate_content(prompt)
    return response.text

def _call_openai(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o", # 또는 gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content