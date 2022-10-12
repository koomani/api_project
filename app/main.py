from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2                          # Database driver
from psycopg2.extras import RealDictCursor
import time
from .DB import engine, get_db
from . import models
from sqlalchemy.orm import Session


# Connect Sqlachemy to postgresql
models.Base.metadata.create_all(bind=engine)

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
                                password='***', 
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
@app.get("/sqlalchemy") 
def test_posts(db: Session = Depends(get_db)):
    return {"Data": "Success"}



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
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # fetch post
    post = cursor.fetchone()
    # commit the change to sql server
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} was Not Found")
    return {"Details": post}


# Delete request
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # fetch post
    post = cursor.fetchone()
    # commit the change to sql server
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} was Not Found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update request
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title= %s, content = %s, published =%s where id = %s RETURNING * """
                    ,(post.title, post.content, post.published, str(id)))
    # fetch post
    post = cursor.fetchone()
    # commit the change to sql server
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} was Not Found")
    return {"data": post}

                            