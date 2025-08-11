from app.models import db, User, Post
def login(client, username='u1', password='x'):
    # Minimal login helper assumes test route or direct session set in test-only app
    with client.session_transaction() as sess:
        sess['_user_id'] = '1'

def test_like_toggle(client, app):
    with app.app_context():
        u = User(id=1, username='u1', email='u1@test', password='x')
        p = Post(content='a', user_id=1)
        db.session.add_all([u,p]); db.session.commit()
    login(client)
    r = client.post(f"/posts/{p.id}/like")
    assert r.status_code in (200, 302)
