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

posts_db_data = dummy_db['post']

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None

class PostModelPartial(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    rating: int | None = None

def find_index(id: int):
    index = None
    data = posts_db_data
    result = [i for i, v in enumerate(data) if v['id'] == id]

    if result:
        index = result[0]
    
    return index


@app.get('/')
def root():
    return { 'message': 'welcome to the API' }

@app.get('/posts')
def get_posts():
    return {
        'data': posts_db_data
    }

@app.get('/posts/{post_id}') # Path parameter
def get_post(
    post_id: int,
    response: Response
):
    result = [i for i in posts_db_data if i['id'] == post_id]

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

    return { "data": post_dict }

@app.delete(
    '/posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_posts(post_id: int):
    index = find_index(post_id)
    
    if not index is None:
        posts_db_data.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT) # send no data back when 204 is the status code

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={ "message": f"Post with ID:{post_id} not found!!!" }
    )

@app.put('/posts/{post_id}')
def update_post(
    post_id: int,
    payload: PostModel
): 
    index = find_index(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )

    posts_db_data.pop(index)

    post_data = payload.model_dump()
    post_data.update({ "id": post_id })

    posts_db_data.append(post_data)

    return { "data": post_data }

@app.patch('/posts/{post_id}')
def patch_post(
    post_id: int,
    payload: PostModelPartial
):
    index = find_index(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ "message": f"Post with ID:{post_id} not found!!!" }
        )
    
    current_post = posts_db_data[index]
    
    post = payload.model_dump()
    post = payload.model_dump(exclude_unset=True) # Note this exclude_unset
    
    current_post.update(post)

    return { "data": current_post }
    