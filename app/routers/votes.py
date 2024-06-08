from typing import Annotated

from fastapi import  APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from app.oauth2 import dep_get_current_user
from app.database import get_db
import app.schema as schema
import app.models as models

router = APIRouter()

@router.post(
    '/votes',
    response_model=schema.Vote | schema.Message,
    status_code=status.HTTP_201_CREATED
)
def vote(
    payload: schema.VoteSubmit,
    current_user: Annotated[models.User, Depends(dep_get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    user_id = current_user.id
    post_id = payload.post_id
    direction = payload.direction

    existing_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not present"
        )


    vote_check_query = db.query(models.Vote).filter(models.Vote.user_id == user_id, models.Vote.post_id == post_id)
    vote_check = vote_check_query.first()
    vote_model = None

    if vote_check is not None and direction == -1:
        vote_check_query.delete()
        db.commit()
        return { 'message': f'Post id:{post_id} deleted' }

    elif vote_check is not None and direction == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already voted"
        )

    elif vote_check is None and direction == 1:
        vote_model = models.Vote(user_id=user_id, post_id=post_id)
        try:
            db.add(vote_model)
            db.commit()
            db.refresh(vote_model)
            return vote_model

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request"
            ) from e

    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request"
            )



    
