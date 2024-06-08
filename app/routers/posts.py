from typing import Annotated, List

from fastapi import Depends, HTTPException, status, Response, APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

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
    response_model=List[schema.PostResponseModeWithVotes]
)
def get_posts(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)],
    limit: int = 10,
    page: int = 1,
    search: str = ''
):
    look_for = '%{0}%'.format(search)
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .filter(models.Post.title.ilike(look_for))\
        .group_by(models.Post.id)\
        .limit(limit)\
        .offset(None if page == 0 else (page - 1) * limit)\
        .all()

    # No idea why FastAPI and SQLAclhemy can't do this on their own
    r = []
    for p, v in result:
        model = schema.PostResponseModeWithVotes(posts=jsonable_encoder(p), votes=v)
        r.append(model)

    return r

@router.get(
    '/{post_id}',
    response_model=schema.PostResponseModeWithVotes
) # Path parameter
def get_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(dep_get_current_user)]
):
    # result = db.query(models.Post).get(post_id)
    result =db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .filter(models.Post.id == post_id)\
        .group_by(models.Post.id)\
        .first()

    if result:
        model = schema.PostResponseModeWithVotes(posts=jsonable_encoder(result[0]), votes=result[1])
        return model
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
    try:
        if payload.user_id is not None:
            new_post = models.Post(**payload.model_dump(exclude_unset=True))
        else:
            new_post = models.Post(user_id=current_user.id, **payload.model_dump(exclude_unset=True))

        db.add(new_post)
        print(new_post)
        db.commit()
        db.refresh(new_post)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error"
        ) from e

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
        result = post.first()
        if result.user_id == current_user.id:
            post.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT) # send no data back when 204 is the status code
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can't delete this post!!!"
        )

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
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can't update this post!!!"
        )

    post_query.update({**payload.model_dump(exclude_defaults=True)}, synchronize_session=False) 
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

    if post_query.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can't update this post!!!"
        )

    update = payload.model_dump(exclude_unset=True)
    post_query.update({**update}, synchronize_session=False)
    db.commit()

    return post_query.first()