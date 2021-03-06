import os
import tempfile
import json
import pytest

from server import server


@pytest.fixture
def client():
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    with server.app.app_context():
        server.init_db()

    yield client

    os.close(db_fd)
    os.unlink(server.app.config['DATABASE'])
    # os.remove('server\idi.db')

def test_healthcheck(client):
    """Start with a blank database."""

    response = client.get('/healthcheck')
    assert response.status_code == 200
    assert b'Server is listening...' in response.data

def test_not_allwoed_method(client):
    """Test wrong method to defined endpoint"""
    response = client.post('/healthcheck',
                            data="something",
                            content_type ='application/json')
    assert response.status_code == 405
    assert b'Method Not Allowed' in response.data

def test_invalid_JSON(client):
    """Test status code 500 from improper JSON on post to raw"""
    response = client.post('/ratings',
                            data="This isn't a json... it's a string!",
                            content_type ='application/json')
    assert response.status_code == 400
    assert b'Bad Request' in response.data



def test_image_rating_insertion(client):
    """Insert new image rating"""

    response = client.post('/ratings',
                             data=json.dumps(dict(userId='9774d56d682e549c', imageId= 'p1', rating= '2')),
                             content_type='application/json')
    assert response.status_code == 200
    assert b'Rating Added' in response.data


def test_image_rating_update(client):
    """update existed image rating"""

    response_init_post = client.post('/ratings',
                             data=json.dumps(dict(userId='9774d56d682e549c', imageId= 'p1', rating= '8')),
                             content_type='application/json')
    assert response_init_post.status_code == 200

    response_update = client.post('/ratings',
                             data=json.dumps(dict(userId='9774d56d682e549c', imageId= 'p1', rating= '5')),
                             content_type='application/json')
    assert response_update.status_code == 200
    assert b'Rating Added' in response_update.data

def test_add_new_user(client):
    """update existed image rating"""

    response = client.post('/users',
                             data=json.dumps({"userId": "9774d56d682e549c", "age": "17", "sex": "male", "date": "13-04-2019 12:08:23"}),
                             content_type='application/json')
    assert response.status_code == 200
    assert b'User Added' in response.data


def test_override_user(client):
    """update existed image rating"""

    response = client.post('/users',
                             data=json.dumps({"userId": "9774d56d682e549c", "age": "17", "sex": "male", "date": "13-04-2019 12:08:23"}),
                             content_type='application/json')
    assert response.status_code == 400
    assert b'user already in DB' in response.data

def test_add_new_action(client):
    """update existed image rating"""

    response = client.post('/actions',
                             data=json.dumps({"userId": "86d7321c-3700-44fe-9c84-f55ed960d4fe", "sessionId": "f1c9ddcd", "timestamp": "04-05-2019 17:23:25", "total_screens": "2", "screen_order": "1", "time_to_pass": "5130", "success": 0, "selected_images": "[p1, p7, p22]", "shown_images": "[p1, p5, p7, p19, p22, p46]", "top_rated_images": "[p1, p5, p46]"}),
                             content_type='application/json')
    assert response.status_code == 200
    assert b'Action registered' in response.data

def test_override_action(client):
    """update existed image rating"""

    response = client.post('/actions',
                             data=json.dumps({"userId": "86d7321c-3700-44fe-9c84-f55ed960d4fe", "sessionId": "f1c9ddcd", "timestamp": "04-05-2019 17:23:25", "total_screens": "2", "screen_order": "1", "time_to_pass": "5130", "success": 0, "selected_images": "[p1, p7, p22]", "shown_images": "[p1, p5, p7, p19, p22, p46]", "top_rated_images": "[p1, p5, p46]"}),
                             content_type='application/json')
    assert response.status_code == 400
    assert b'Action has not registered' in response.data




