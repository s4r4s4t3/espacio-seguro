from io import BytesIO
from app.models import db, User
def login(client, user_id='1'):
    with client.session_transaction() as sess:
        sess['_user_id'] = user_id

def test_create_story(client, app):
    with app.app_context():
        u = User(id=1, username='u1', email='u1@test', password='x')
        db.session.add(u); db.session.commit()
    login(client)
    data = {'caption':'hola', 'story_image': (BytesIO(b'fakeimg'), 'a.jpg')}
    r = client.post('/stories/create', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert r.status_code in (200, 302)
