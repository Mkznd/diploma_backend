from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from video_generation.main import generate_video

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(topic: str, length: int):
    return FileResponse(
        generate_video(topic, length),
        media_type="video/mp4",
    )
