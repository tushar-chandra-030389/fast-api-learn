from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Literal



class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_orm = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = 'bearer'

class TokenPayload(BaseModel):
    id: str | None = None


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    user_id: int | None = None
class PostModelPartial(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    user_id: int | None = None

class PostResponseMode(PostModel):
    id: int
    created_at: datetime
    owner: UserResponse
    class Config:
        from_orm = True
