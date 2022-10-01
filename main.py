from fastapi import FastAPI

# Intialize new api instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Intialize our web server