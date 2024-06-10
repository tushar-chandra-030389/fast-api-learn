import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from termcolor import colored

from app.main import app
from app.config import config
from app.models import Base as ModelsBase
from app.database import get_db

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
@pytest.fixture(scope="module")
def db():
    ModelsBase.metadata.drop_all(bind=test_engine)
    ModelsBase.metadata.create_all(bind=test_engine)

    dbs = SessionTest()
    try:
        yield dbs
    finally:
        dbs.close()

# fixture to return test client
@pytest.fixture(scope="module")
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
    
