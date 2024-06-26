from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import Column, String

from app.database import get_db
import app.models as models
import app.schema as schema
import app.security as security
import app.oauth2 as oauth2

router = APIRouter(
    tags=['authentication']
)
 

@router.post(
    '/login',
    response_model=schema.TokenResponse
)
def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
    db: Annotated[Session, Depends(get_db)]
):
    user_query = db.query(models.User).filter(models.User.email == payload.username)
    user_model = user_query.first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user or password."
        )
    
    is_pass_valid = security.verify_password(payload.password, str(user_model.password))

    if is_pass_valid is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user or password."
        )

    token_payload = schema.TokenPayload(id=str(user_model.id))
    token = oauth2.create_token(token_payload)

    return { "access_token": token }
