from math import cos, radians, sin, sqrt, atan2
from typing import List, Optional

from sqlalchemy.orm import Session

from app.constants import CONTENT_TYPE_MAP
from app.models import TourLocation
from app.schemas.chat import NearbyPlaceResponse


# 지구 평균 반지름
EARTH_RADIUS_KM = 6371.0088


def calculate_distance_km(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
) -> float:
    """
    두 위도·경도 사이의 거리를 Haversine 공식으로 계산한다.

    반환값:
        거리(km)
    """

    start_lat_rad = radians(start_lat)
    start_lon_rad = radians(start_lon)
    end_lat_rad = radians(end_lat)
    end_lon_rad = radians(end_lon)

    lat_difference = end_lat_rad - start_lat_rad
    lon_difference = end_lon_rad - start_lon_rad

    haversine_value = (
        sin(lat_difference / 2) ** 2
        + cos(start_lat_rad)
        * cos(end_lat_rad)
        * sin(lon_difference / 2) ** 2
    )

    central_angle = 2 * atan2(
        sqrt(haversine_value),
        sqrt(1 - haversine_value),
    )

    return EARTH_RADIUS_KM * central_angle


def make_address(
    addr1: Optional[str],
    addr2: Optional[str],
) -> Optional[str]:
    """
    기본 주소와 상세 주소를 하나의 문자열로 합친다.
    """

    address_parts = []

    if addr1:
        address_parts.append(addr1.strip())

    if addr2:
        address_parts.append(addr2.strip())

    if not address_parts:
        return None

    return " ".join(address_parts)


def get_nearby_places(
    db: Session,
    lat: float,
    lon: float,
    radius_km: float = 2.0,
    limit: int = 10,
) -> List[NearbyPlaceResponse]:
    """
    사용자 위치 주변의 관광지를 거리순으로 조회한다.

    1. 위도·경도 범위로 후보 장소를 먼저 조회한다.
    2. 각 후보 장소의 실제 거리를 계산한다.
    3. 지정된 반경 안에 있는 장소만 남긴다.
    4. 거리순으로 정렬한 후 limit만큼 반환한다.
    """

    # 위도 1도는 약 111km
    latitude_delta = radius_km / 111.0

    # 경도 1도의 거리는 위도에 따라 달라진다.
    longitude_km_per_degree = 111.320 * abs(cos(radians(lat)))

    # 극지방처럼 경도 계산값이 지나치게 작아지는 경우를 방지한다.
    if longitude_km_per_degree < 0.001:
        longitude_delta = 180.0
    else:
        longitude_delta = min(
            radius_km / longitude_km_per_degree,
            180.0,
        )

    # 전체 데이터를 모두 읽지 않고,
    # 사용자의 위치 주변 사각형 범위만 DB에서 먼저 조회한다.
    candidate_locations = (
        db.query(TourLocation)
        .filter(
            TourLocation.mapx.isnot(None),
            TourLocation.mapy.isnot(None),
            TourLocation.mapy.between(
                lat - latitude_delta,
                lat + latitude_delta,
            ),
            TourLocation.mapx.between(
                lon - longitude_delta,
                lon + longitude_delta,
            ),
        )
        .all()
    )

    nearby_places: List[NearbyPlaceResponse] = []

    for location in candidate_locations:
        # mapy는 위도, mapx는 경도
        place_lat = float(location.mapy)
        place_lon = float(location.mapx)

        distance_km = calculate_distance_km(
            start_lat=lat,
            start_lon=lon,
            end_lat=place_lat,
            end_lon=place_lon,
        )

        # 실제 원형 반경 밖에 있는 장소는 제외한다.
        if distance_km > radius_km:
            continue

        category_name = CONTENT_TYPE_MAP.get(
            location.contenttypeid,
            "기타",
        )

        nearby_places.append(
            NearbyPlaceResponse(
                contentid=str(location.contentid),
                name=location.title,
                category=category_name,
                address=make_address(
                    location.addr1,
                    location.addr2,
                ),
                lat=place_lat,
                lng=place_lon,
                distance_km=round(distance_km, 2),
                image=location.firstimage,
            )
        )

    # 가까운 장소부터 정렬
    nearby_places.sort(
        key=lambda place: place.distance_km
    )

    return nearby_places[:limit]


def build_places_context(
    places: List[NearbyPlaceResponse],
) -> str:
    """
    주변 관광지 목록을 AI에게 전달할 문자열로 변환한다.
    """

    if not places:
        return "현재 검색 반경 안에 등록된 주변 장소가 없습니다."

    context_lines = []

    for index, place in enumerate(places, start=1):
        address = place.address or "주소 정보 없음"

        context_lines.append(
            f"{index}. 장소명: {place.name}\n"
            f"   분류: {place.category}\n"
            f"   주소: {address}\n"
            f"   사용자 위치로부터 거리: {place.distance_km}km"
        )

    return "\n".join(context_lines)