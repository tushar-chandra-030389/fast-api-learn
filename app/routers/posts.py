from typing import Annotated, List

from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session

import app.models as models
import app.schema as schema
from app.database import get_db
from app.oauth2 import dep_get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

@router.get(
    '',
    response_model=List[schema.PostResponseMode]
)
def get_posts(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
):
    posts = db.query(models.Post).all()
    return posts

@router.get(
    '/{post_id}',
    response_model=schema.PostResponseMode
) # Path parameter
def get_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
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

@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.PostResponseMode
)
def save_post(
    payload: schema.PostModel,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
):
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_posts(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
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

@router.put(
    '/{post_id}',
    response_model=schema.PostResponseMode
)
def update_post(
    post_id: int,
    payload: schema.PostModel,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
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

@router.patch(
    '/{post_id}',
    response_model=schema.PostResponseMode
)
def patch_post(
    post_id: int,
    payload: schema.PostModelPartial,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
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