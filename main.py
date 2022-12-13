from fastapi import FastAPI

app = FastAPI()


@app.get("/login")
async def root():
    return {"message": "Hello World"}