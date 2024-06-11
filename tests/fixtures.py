import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from termcolor import colored

from app.main import app
from app.config import config
from app.models import Base as ModelsBase
import app.schema as schema
import app.models as models
from app.database import get_db
from app.oauth2 import create_token

SQLALCHEMY_DATABASE_URL = f'postgresql://{config.database_username}:{config.database_password}@{config.database_hostname}/{config.database_name_test}'

test_engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)
Base = declarative_base()

# # Dependency
# def get_test_db():
#     db = SessionTest()
#     try:
#         yield db
#     finally:
#         db.close()

# # override dependecy to get the DB session.
# app.dependency_overrides[get_db] = get_test_db


# fixture to return db session
@pytest.fixture(scope="function")
def db():
    ModelsBase.metadata.drop_all(bind=test_engine)
    ModelsBase.metadata.create_all(bind=test_engine)

    dbs = SessionTest()
    try:
        yield dbs
    finally:
        dbs.close()

# fixture to return test client
@pytest.fixture(scope="function")
def tc(db):
    tc = TestClient(app)

    # Dependency
    def get_test_db():
        try:
            yield db
        finally:
            db.close()
    
    # override dependecy to get the DB session.
    app.dependency_overrides[get_db] = get_test_db

    yield tc

@pytest.fixture
def test_user(tc):
    user_data = { 'email': 'tushar2@gmail.com', 'password': 'password' }
    res = tc.post('/users', json=user_data)
    res_json = res.json()

    assert res.status_code == 201
    return { **res_json, 'password': user_data['password'] }

@pytest.fixture
def get_token(test_user):
    payload = schema.TokenPayload(id=str(test_user['id']))
    return create_token(payload=payload)

@pytest.fixture
def atc(tc, get_token):
    tc.headers = {
        **tc.headers,
        "Authorization": f"Bearer {get_token}"   
    }

    return tc

@pytest.fixture
def test_posts(test_user, db: Session):
    user_id = test_user['id']

    posts = [
        { 'title': 'title 1', 'content': 'Content 1' },
        { 'title': 'title 2', 'content': 'Content 2' },
        { 'title': 'title 3', 'content': 'Content 3' },
        { 'title': 'title 4', 'content': 'Content 4' }
    ]

    post_models_map = map(lambda p: models.Post(**p, user_id=user_id), posts)
    post_models = list(post_models_map)

    db.add_all(post_models)
    db.commit()

    p = db.query(models.Post).all()

    return p
