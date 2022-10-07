from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Intialize new api instance
app = FastAPI()

# Post creation skeleton
class Post(BaseModel):
    title: str
    content: str
    published : bool = True

# Database connection
while True:
    try:
        conn = psycopg2.connect(
                                host='localhost',
                                database='api_project', 
                                user='postgres', 
                                password='Python@1234', 
                                cursor_factory=RealDictCursor
                                )
        cursor = conn.cursor()
        print("Successfully connected")
        break
    except Exception as e:
        print(" Failed to connection", str(e))
        time.sleep(3)


# Store the post in memory till database will be created
the_posts = [
            {"title": "title post", "content": "content post", "id": 1},
            {"title": "Animals", "content": "Python", "id": 2},
            ]


# Get request
@app.get("/posts", status_code=status.HTTP_200_OK)       # Path app operation or root
def get_posts() -> dict:
    cursor.execute(""" SELECT * FROM posts """)
    # fetch all 
    return {"Data": cursor.fetchall()}


# Create request
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post) -> dict:
    cursor.execute(""" INSERT INTO  posts (title, content, published)
                        VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # fetch post
    post = cursor.fetchone()

    # commit the change to sql server
    conn.commit()
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

                            