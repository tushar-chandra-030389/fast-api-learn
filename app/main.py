import time
import os
import signal

from fastapi import (FastAPI)
import psycopg2
from psycopg2.extras import RealDictCursor

import app.models as models
from app.database import engine
from app.routers import posts, users

models.Base.metadata.create_all(bind=engine)


def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)
    print('Shutting down server')

DB_ATTEMPT_COUNTER = 0
while DB_ATTEMPT_COUNTER <= 2:
    try:
        DB_ATTEMPT_COUNTER = DB_ATTEMPT_COUNTER + 1
        db_connection = psycopg2.connect(
            host='localhost',
            dbname='fastapi',
            user='postgres',
            password='root',
            cursor_factory=RealDictCursor
        )
        db_cursor = db_connection.cursor()
        print('DB Connection successful!!!')
        break
    except psycopg2.Error as e:
        print('DB Connection failed!!!')
        print(e)
        if DB_ATTEMPT_COUNTER >= 2:
            shutdown_server()
        time.sleep(2)


tags_metadata = [
    {
        "name": "root",
        "description": "Basic config routes!!!",
    },
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "posts",
        "description": "User posts realted endpoints"
    },
]

app = FastAPI(
    openapi_tags= tags_metadata
)

app.include_router(users.router)
app.include_router(posts.router)

@app.get(
    '/',
    tags=['root']
)
def root():
    return { 'message': 'welcome to the API' }
