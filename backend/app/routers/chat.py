from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import (
    AIConfigurationError,
    AIServiceError,
    get_ai_response,
)
from app.services.chat_service import (
    build_places_context,
    get_nearby_places,
)


router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="AI 관광 챗봇",
    description=(
        "사용자의 질문과 현재 위치를 받아 주변 관광지를 조회하고, "
        "AI가 관광 안내 답변을 생성합니다."
    ),
)
def chat_with_bot(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    """
    사용자 위치를 기반으로 주변 관광지를 조회한 뒤,
    관광지 정보와 사용자 질문을 AI에게 전달한다.
    """

    try:
        # 1. 기존 tour_locations 테이블에서 주변 관광지 조회
        nearby_places = get_nearby_places(
            db=db,
            lat=request.lat,
            lon=request.lon,
            radius_km=request.radius_km,
            limit=request.limit,
        )

        # 2. 주변 관광지 목록을 AI가 읽을 수 있는 문자열로 변환
        places_context = build_places_context(
            places=nearby_places,
        )

        # 3. 사용자 질문과 주변 관광지 정보를 AI에 전달
        ai_reply = get_ai_response(
            user_query=request.user_query,
            places_context=places_context,
        )

        # 4. AI 답변과 주변 관광지 목록 반환
        return ChatResponse(
            reply=ai_reply,
            nearby_places=nearby_places,
        )

    except AIConfigurationError as exc:
        # API 키나 모델명 등 서버 환경설정이 잘못된 경우
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    except AIServiceError as exc:
        # Gemini 또는 OpenAI 호출에 실패한 경우
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        # DB 조회 등 예상하지 못한 서버 오류
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="챗봇 요청을 처리하는 중 오류가 발생했습니다.",
        ) from exc