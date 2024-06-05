from typing import Annotated

from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException
)
from pydantic import BaseModel
from random import randrange

app = FastAPI()

dummy_db = {
    "post": [
        { "id": 1, "title": "Title 1", "content": "Post content 1" },
        { "id": 2, "title": "Title 2", "content": "Post content 2. Post content 2." },
        { "id": 3, "title": "Title 3", "content": "Post content 3. Post content 3. Post content 3" }
    ]
}

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


@app.get('/')
def root():
    return { 'message': 'welcome to the API' }

@app.get('/posts')
def get_posts():
    return {
        'data': dummy_db['post']
    }

@app.get('/posts/{post_id}') # Path parameter
def get_post(
    post_id: int,
    response: Response
):
    result = [i for i in dummy_db['post'] if i['id'] == post_id]

    if result:
        return { "data": result[0] }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Post with ID:{post_id} not found!!!",
                "data": []
            }
        )

@app.post(
    '/posts',
    status_code=status.HTTP_201_CREATED
)
def save_post(post: PostModel):
    post_dict = post.model_dump()
    post_dict.update({ "id": randrange(1, 1000000) })
    dummy_db['post'].append(post_dict)

    return {
        "data": post_dict
    }

@app.delete(
    '/posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_posts(post_id: int):
    index = None
    search_result = [i for i, v in enumerate(dummy_db['post']) if v['id'] == post_id]

    if search_result:
        index = search_result[0]
        dummy_db['post'].pop(index)

    if not index is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT) # send no data back when 204 is the status code

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": f"Post with ID:{post_id} not found!!!",
        }
    )
