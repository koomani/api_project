from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session


# Connect Sqlachemy to postgresql
models.Base.metadata.create_all(bind=engine)

# Intialize new api instance
app = FastAPI()

# Get request
@app.get("/posts", status_code=status.HTTP_200_OK)        # Path app operation or root
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.post).all()                   # => select * from posts
    return {"Data": posts}


# Create request
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(db: Session = Depends(get_db)):

    #return {"Posts": post}
    pass
'''

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

'''
