from fastapi.testclient import TestClient

from .fixtures import atc, tc, get_token, test_user, db, test_posts

import app.schema as schema

def test_get_all_posts(atc, test_posts):
    res = atc.get('/posts')
    res_json = res.json()

    assert res.status_code == 200
    assert len(res_json) == 4

def test_unanuth_get_all_posts(tc, test_posts):
    res = tc.get('/posts')
    assert res.status_code == 401

def test_get_one_post(atc, test_posts):
    res = atc.get(f'/posts/{test_posts[0].id}')

    res_json = res.json()
    assert res.status_code == 200
    assert res_json['posts']['id'] == test_posts[0].id

def test_get_one_post_not_exists(atc, test_posts):
    res = atc.get('/posts/9999')

    assert res.status_code == 404

def test_unanuth_get_one_post(tc, test_posts):
    res = tc.get(f'/posts/{test_posts[0].id}')

    assert res.status_code == 401

def test_create_post(atc, test_posts, test_user):
    res =atc.post('/posts', json={'title': 'title new', 'content': 'content new'})
    res_json = res.json()

    res_schema = schema.PostResponseMode(**res_json)
    assert res.status_code == 201
    assert res_schema.title == 'title new'
    assert res_schema.content == 'content new'
    assert res_schema.owner.email == test_user['email']

def test_unauth_delete_post(tc, test_posts):
    res = tc.delete(f'/posts/{test_posts[0].id}')

    assert res.status_code == 401

def test_delete_post(atc, test_posts):
    res = atc.delete(f'/posts/{test_posts[0].id}')
    res_get = atc.get('/posts')
    res_get_json = res_get.json()

    assert res.status_code == 204
    assert len(res_get_json) == 3

