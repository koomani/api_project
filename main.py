from fastapi import FastAPI

# intialize new api instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# intialize our web server