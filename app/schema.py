from pydantic import BaseModel

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True

class PostModelPartial(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None