from app.services import post_service
from app.schemas.post import PostCreate, PostUpdate, DeleteRequest


def test_create_get_update_delete_post(db_session):
    # create
    create_in = PostCreate(title="t1", content="c1", category="cat", password="pw")
    post = post_service.create_post(db_session, create_in)

    assert post.id is not None
    assert post.title == "t1"

    # get_posts
    posts = post_service.get_posts(db_session)
    assert any(p.id == post.id for p in posts)

    # get_post
    fetched = post_service.get_post(db_session, post.id)
    assert fetched.id == post.id

    # update (wrong password)
    upd = PostUpdate(title="t2", content="c2", category="cat2", password="wrong")
    try:
        post_service.update_post(db_session, post.id, upd)
        assert False, "should have raised"
    except Exception:
        pass

    # update (correct)
    upd.password = "pw"
    upd.title = "t-upd"
    updated = post_service.update_post(db_session, post.id, upd)
    assert updated.title == "t-upd"

    # delete (wrong pw)
    try:
        post_service.delete_post(db_session, post.id, DeleteRequest(password="no"))
        assert False, "should have raised"
    except Exception:
        pass

    # delete (correct)
    resp = post_service.delete_post(db_session, post.id, DeleteRequest(password="pw"))
    assert isinstance(resp, dict) and "삭제" in resp.get("message", "")
