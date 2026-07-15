from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    프론트엔드에서 챗봇 API로 전달하는 요청 데이터.
    """

    # 사용자가 입력한 질문
    user_query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="사용자가 챗봇에게 입력한 질문",
    )

    # 사용자 현재 위치의 위도
    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="사용자의 현재 위도",
    )

    # 사용자 현재 위치의 경도
    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="사용자의 현재 경도",
    )

    # 주변 관광지를 검색할 반경
    radius_km: float = Field(
        default=2.0,
        gt=0,
        le=20,
        description="주변 관광지 검색 반경(km)",
    )

    # AI에게 전달할 최대 관광지 개수
    limit: int = Field(
        default=10,
        ge=1,
        le=30,
        description="조회할 주변 관광지 최대 개수",
    )


class NearbyPlaceResponse(BaseModel):
    """
    챗봇 응답에 포함되는 주변 관광지 정보.
    """

    contentid: str
    name: str
    category: str
    address: Optional[str] = None
    lat: float
    lng: float
    distance_km: float
    image: Optional[str] = None


class ChatResponse(BaseModel):
    """
    챗봇 API가 프론트엔드로 반환하는 최종 응답.
    """

    # AI가 생성한 답변
    reply: str

    # AI 답변을 만들 때 참고한 주변 관광지 목록
    nearby_places: List[NearbyPlaceResponse]