from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError

# openssl rand -hex 32
SECRET_KEY = '16b032d1cf1dba6876ff05b3126715910f8834189105dffa27016693ebaf0a04'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(payload: dict):
    payload_copy = payload.copy()

    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_copy.update({ "exp": expire_time })
    token = jwt.encode(payload=payload_copy, algorithm=ALGORITHM, key=SECRET_KEY)

    return token