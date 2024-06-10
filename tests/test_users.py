import jwt
from termcolor import colored
import pytest

import app.schema as schema
from app.config import config
from .fixtures import tc, db

@pytest.fixture
def insert_login_user(tc):
    user_data = { 'email': 'tushar2@gmail.com', 'password': 'password' }
    res = tc.post('/users', json=user_data)
    res_json = res.json()

    assert res.status_code == 201
    return { **res_json, 'password': user_data['password'] }


def test_root(tc):
    res = tc.get('/')
    # print(colored(res.__dict__, 'red'))
    # print(colored(res.json(), 'red'))
    assert res.json().get('message') == 'welcome to the API'
    assert res.status_code == 200


def test_add_user(tc):
    res = tc.post('/users', json={"email": "tushar@gmail.com", "password": "password"})
    user_res = schema.UserResponse(**res.json())

    assert res.status_code == 201
    assert user_res.email == "tushar@gmail.com"

def test_login_user(insert_login_user, tc):
    res = tc.post('/login', data={'username': insert_login_user['email'], 'password': insert_login_user['password']})
    token_res = schema.TokenResponse(**res.json())
    assert res.status_code == 200

    token_payload = jwt.decode(
        jwt=token_res.access_token,
        key=config.secret_key,
        algorithms=[config.algorithm]
    )
    assert int(token_payload['id']) == insert_login_user['id']
    assert token_res.token_type == 'bearer'
