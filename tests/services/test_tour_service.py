from app.services import tour_service
from app.models import TourLocation


def test_get_places_by_region(db_session):
    # create sample locations
    loc1 = TourLocation(contentid="c1", contenttypeid="12", title="Place A", addr1="경상북도 구미시 원평동", mapx=128.1, mapy=36.1)
    loc2 = TourLocation(contentid="c2", contenttypeid="39", title="Place B", addr1="경상북도 구미시 송정동", mapx=128.2, mapy=36.2)
    db_session.add_all([loc1, loc2])
    db_session.commit()

    res = tour_service.get_places_by_region(db_session, "원평동")
    assert any(r.contentid == "c1" for r in res)
    # 송정동도 관계로 포함되어야 함
    assert any(r.contentid == "c2" for r in res)
