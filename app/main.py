from typing import Annotated, List
from random import randrange
import time
import os
import signal

from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends
)
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schema, security
from .database import engine, get_db


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

app = FastAPI()

@app.get('/')
def root():
    return { 'message': 'welcome to the API' }

@app.get(
    '/posts',
    response_model=List[schema.PostResponseMode]
)
def get_posts(db: Annotated[Session, Depends(get_db)]):
    posts = db.query(models.Post).all()
    return posts

@app.get(
    '/posts/{post_id}',
    response_model=schema.PostResponseMode
) # Path parameter
def get_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    # result = db.query(models.Post).get(post_id)
    result =db.query(models.Post).filter(models.Post.id == post_id).first()

    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Post with ID:{post_id} not found!!!",
            }
        )

@app.post(
    '/posts',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.PostResponseMode
)
def save_post(
    payload: schema.PostModel,
    db: Annotated[Session, Depends(get_db)]
):
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.delete(
    '/posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_posts(
    post_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT) # send no data back when 204 is the status code

@app.put(
    '/posts/{post_id}',
    response_model=schema.PostResponseMode
)
def update_post(
    post_id: int,
    payload: schema.PostModel,
    db: Annotated[Session, Depends(get_db)]
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )

    post_query.update({**payload.model_dump()}, synchronize_session=False) 
    db.commit()

    return post_query.first()

@app.patch(
    '/posts/{post_id}',
    response_model=schema.PostResponseMode
)
def patch_post(
    post_id: int,
    payload: schema.PostModelPartial,
    db: Annotated[Session, Depends(get_db)]
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )

    update = payload.model_dump(exclude_unset=True)
    post_query.update({**update}, synchronize_session=False)
    db.commit()

    return post_query.first()

##################  User ##################

@app.post(
    '/users',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.UserResponse
)
def create_user(
    payload: schema.UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
    payload_dict = payload.model_dump()
    user_model = models.User(**payload_dict)

    user_model.password = security.hash_password(str(user_model.password))

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model

@app.get(
    '/users/{user_id}',
    response_model=schema.UserResponse
)
def get_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id:{user_id} not found"
    )