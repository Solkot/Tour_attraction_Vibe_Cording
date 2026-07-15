from sqlalchemy import text

def get_nearby_spots(db, lat, lon, radius_km=2.0):
    # 서브쿼리를 사용하여 먼저 거리를 계산하고, 
    # 그 결과를 가진 'sub' 테이블에서 distance를 필터링합니다.
    query = """
        SELECT * FROM (
            SELECT *, 
            (6371 * acos(cos(radians(:lat)) * cos(radians(mapy)) * cos(radians(mapx) - radians(:lon)) + sin(radians(:lat)) * sin(radians(mapy)))) AS distance
            FROM spots
        ) AS sub
        WHERE distance <= :radius
        ORDER BY distance ASC
    """
    
    # db.execute를 사용할 때 매개변수 바인딩 확인 (딕셔너리 형태로 전달)
    return db.execute(
        text(query), 
        {"lat": lat, "lon": lon, "radius": radius_km}
    ).fetchall()