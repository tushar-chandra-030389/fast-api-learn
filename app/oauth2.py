from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schema as schema
import app.models as models
import app.database as database

# openssl rand -hex 32
SECRET_KEY = '16b032d1cf1dba6876ff05b3126715910f8834189105dffa27016693ebaf0a04'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_token(payload: schema.TokenPayload):
    payload_copy = payload.model_dump()

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_copy.update({ "exp": expire_time })
    token = jwt.encode(payload=payload_copy, algorithm=ALGORITHM, key=SECRET_KEY)

    return token


def verify_access_token(token: str, outh_exception: Exception):
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload['id'] is None:
            raise outh_exception
        
        model = schema.TokenPayload(id=payload['id'])

        return model
    except:
        raise outh_exception
    
def dep_get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(database.get_db)]
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload: schema.TokenPayload = verify_access_token(token, credential_exception)

    user_model = db.query(models.User).filter(models.User.id == payload.id).first()

    if user_model is None:
        raise credential_exception

    return user_model
