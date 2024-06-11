import jwt
from termcolor import colored
import pytest

import app.schema as schema
from app.config import config
from .fixtures import tc, db, test_user


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

def test_login_user(test_user, tc):
    res = tc.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    token_res = schema.TokenResponse(**res.json())
    assert res.status_code == 200

    token_payload = jwt.decode(
        jwt=token_res.access_token,
        key=config.secret_key,
        algorithms=[config.algorithm]
    )
    assert int(token_payload['id']) == test_user['id']
    assert token_res.token_type == 'bearer'

@pytest.mark.parametrize(
    'email, password, status_code, error_message', [
        ['tushar2@gmail.com', 'wrong', 403, 'Invalid user or password.'],
        ['tushar22@gmail.com', 'password', 403, 'Invalid user or password.'],
        ['tushar22@gmail.com', 'wrong', 403, 'Invalid user or password.'],
        ['tushar22@gmail.com', None, 422, 'Invalid user or password.'],
        [None, 'password', 422, 'Invalid user or password.'],
    ]
)
def test_invalid_login(test_user, tc, email, password, status_code, error_message):
    res = tc.post('/login', data={ "username": email, 'password': password })
    response_json = res.json()

    assert res.status_code == status_code

    if res.status_code == 403:
        assert response_json['detail'] == 'Invalid user or password.'
