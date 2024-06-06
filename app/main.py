from typing import Annotated
from random import randrange
import time
import os
import signal

from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException
)
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

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

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None

class PostModelPartial(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    rating: int | None = None

@app.get('/')
def root():
    return { 'message': 'welcome to the API' }

@app.get('/posts')
def get_posts():
    db_cursor.execute('''SELECT * FROM public.post''')
    posts = db_cursor.fetchall()
    
    return {
        'data': posts
    }

@app.get('/posts/{post_id}') # Path parameter
def get_post(post_id: int):
    db_cursor.execute('''SELECT * FROM public.post WHERE id = %s ''', (post_id, ))
    result = db_cursor.fetchone()
    print(result)

    if result:
        return { "data": result }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Post with ID:{post_id} not found!!!",
                "data": []
            }
        )

@app.post(
    '/posts',
    status_code=status.HTTP_201_CREATED
)
def save_post(payload: PostModel):
    db_cursor.execute(
        '''INSERT INTO public.post (title, "content", published) VALUES (%s, %s, %s) RETURNING *''',
        (payload.title, payload.content, payload.published)
    )
    post = db_cursor.fetchone()
    db_connection.commit()
    return { "data": post }

@app.delete(
    '/posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_posts(post_id: int):
    try:
        db_cursor.execute('''
            DELETE FROM public.post WHERE id = %s
        ''', (post_id, ))
        db_connection.commit()
    except psycopg2.Error as ex:
        raise ex

    rows_deleted = db_cursor.rowcount # get effected rows

    if (rows_deleted == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT) # send no data back when 204 is the status code


@app.put('/posts/{post_id}')
def update_post(
    post_id: int,
    payload: PostModel
):
    db_cursor.execute('''
        UPDATE public.post SET
            title=%s, "content"=%s, published=%s
            WHERE id = %s RETURNING *
    ''', (payload.title, payload.content, payload.published, post_id))
    updated_post = db_cursor.fetchone()
    rows_effected = db_cursor.rowcount
    db_connection.commit()

    if rows_effected == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )
    
    return { "data": updated_post }

@app.patch('/posts/{post_id}')
def patch_post(
    post_id: int,
    payload: PostModelPartial
):
    payload_keys = payload.model_dump(exclude_unset=True).keys()
    payload_values = payload.model_dump(exclude_unset=True).values()

    set_clauses = []

    for k in payload_keys:
        set_clauses.append(f'{k}=%s')

    set_clause = ', '.join(set_clauses)

    query = f'UPDATE public.post SET {set_clause} WHERE id=%s RETURNING *'
    values_tuple = tuple(payload_values) + (post_id, )
    print(query, values_tuple)

    try:
        db_cursor.execute(query, values_tuple)
        patched_post = db_cursor.fetchone()
        db_connection.commit()
        updated_rows = db_cursor.rowcount
    except psycopg2.Error as er:
        raise er

    if updated_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )
    else:
        return { "data": patched_post }
