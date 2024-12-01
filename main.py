from fastapi import FastAPI
from video_generation.main import generate_video

app = FastAPI()


@app.get("/")
async def root():
    return generate_video("Black hole formation", 5)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
