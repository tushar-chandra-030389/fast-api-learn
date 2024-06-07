from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

import app.models as models
import app.schema as schema
import app.security as security
from app.database import get_db
from app.oauth2 import dep_get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post(
    '',
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

@router.get(
    '/me',
    response_model=schema.UserResponse
)
def get_current_user(current_user: Annotated[models.User, Depends(dep_get_current_user)]):
    return current_user

@router.get(
    '/{user_id}',
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
