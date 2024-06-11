import time
import os
import signal
from functools import wraps  # For retry decorator

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import config

SQLALCHEMY_DATABASE_URL = f'postgresql://{config.database_username}:{config.database_password}@{config.database_hostname}:{config.database_port}/{config.database_name}'

def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)
    print('Shutting down server')

# test this
# Retry decorator (can be customized)
def retry(max_retries=3, on_exception=OperationalError, delay=2):
    """
    Retries a function call up to `max_retries` times on specific exceptions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except on_exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    print(f"Connection failed. Retrying attempt {retries}/{max_retries}...")
                    time.sleep(delay)
        return wrapper
    return decorator

time.sleep(5)

@retry()
def get_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return engine

engine = get_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



