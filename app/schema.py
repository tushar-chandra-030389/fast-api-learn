from pydantic import BaseModel, EmailStr
from datetime import datetime
class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True

class PostModelPartial(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class PostResponseMode(PostModel):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
