from fastapi import FastAPI, Response, status, HTTPException
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

# Store the post in memory till database will be created
# TODO create database server
the_posts = [
            {"title": "title post", "content": "content post", "id": 1},
            {"title": "Animals", "content": "Python", "id": 2},
            ]


# Get request
@app.get("/posts", status_code=status.HTTP_200_OK)       # Path app operation or root
def get_data() -> dict:
    return {"Posts": the_posts[1]}


# Create request
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post) -> dict:
    post = new_post.dict()
    post["id"] = randrange(0, 1000000000)
    the_posts.append(post)
    return {"Posts": post}


@app.get("/posts/latest", status_code=status.HTTP_200_OK)
def get_last_post():
    post = the_posts[len(the_posts)- 1]
    return {"Details": post}


# Get request with id
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)     
def get_post(id: int, response: Response):       
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} was Not Found")
    return {"Details": post}

def find_post(id: int) -> Post:
    for p in the_posts:
        if p["id"] == id:
            return p


# Delete request
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} was Not Found")
    the_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def find_index_post(id: int):
    for i, p in enumerate(the_posts):
        if p["id"] == id:
            return i


# Update request
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} was Not Found")
    post = post.dict()
    post["id"] == id
    the_posts[index] = post
    return {"Data": post}

                            