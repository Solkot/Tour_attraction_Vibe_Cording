from app.services import comment_service, post_service
from app.schemas.post import PostCreate, DeleteRequest
from app.schemas.comment import CommentCreate


def test_create_get_delete_comment(db_session):
    # create a post first
    p = PostCreate(title="pt", content="pc", category="cat", password="pw")
    post = post_service.create_post(db_session, p)

    # create comment
    c_in = CommentCreate(author="a", content="hello", password="cpw")
    comment = comment_service.create_comment(db_session, post.id, c_in)
    assert comment.id is not None

    # get comments
    comments = comment_service.get_comments(db_session, post.id)
    assert any(c.id == comment.id for c in comments)

    # delete wrong pw
    try:
        comment_service.delete_comment(db_session, comment.id, DeleteRequest(password="no"))
        assert False
    except Exception:
        pass

    # delete correct
    res = comment_service.delete_comment(db_session, comment.id, DeleteRequest(password="cpw"))
    assert isinstance(res, dict) and "삭제" in res.get("message", "")
