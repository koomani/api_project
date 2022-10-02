from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

# Intialize new api instance
app = FastAPI()


# Post creation skeleton
class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional[int] = None

# Store the post in memory
the_posts = [
            {"title": "title post", "content": "content post", "id": 1},
            {"title": "Animals", "content": "Python", "id": 2},
            ]

def find_post(id: int) -> Post:
    for p in the_posts:
        if p["id"] == id:
            return p

# Path app operation or root
@app.get("/posts")
def get_data() -> dict:
    return {"Posts": the_posts[1]}

# Testing posts from postman 
@app.post("/posts")
def create_posts(new_post: Post) -> dict:
    post = new_post.dict()
    post["id"] = randrange(0, 1000000000)
    the_posts.append(post)
    return {"Posts": post}


@app.get("/posts/latest")
def get_last_post():
    post = the_posts[len(the_posts)- 1]
    return {"Details": post}


# Id is the path parameter (always returns back as str type)
@app.get("/posts/{id}")     
def get_post(id: int):           # fastapi convert it into int type
    post = find_post(id)
    return {"Details": post}


                            