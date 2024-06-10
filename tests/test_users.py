from termcolor import colored

import app.schema as schema
from .fixtures import tc, db

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

def test_login_user(tc):
    res = tc.post('/login', data={'username': 'tushar@gmail.com', 'password': 'password'})
    token_res = schema.TokenResponse(**res.json())
    
    assert res.status_code == 200
    assert token_res.access_token is not None