from fastapi import (FastAPI)
from fastapi.middleware.cors import CORSMiddleware

import app.models as models
from app.database import engine
from app.routers import posts, users, auth, votes

models.Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        "name": "root",
        "description": "Basic config routes!!!",
    },
    {
        "name": "authentication",
        "description": "Authentication routes!!!",
    },
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "posts",
        "description": "User posts realted endpoints"
    },
]

origins = '*'

app = FastAPI(
    openapi_tags= tags_metadata
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    '/',
    tags=['root']
)
def root():
    return { 'message': 'welcome to the API' }
