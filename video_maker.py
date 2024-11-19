import math

from moviepy.editor import *


def make_video(n: int, dir_name: str, voice_length: float, name: str):
    duration = voice_length / n

    clips = list(
        [
            ImageClip(f"{dir_name}/images/{i}.png").set_duration(duration).fadein(1)
            for i in range(n)
        ]
    )
    video_clip = concatenate_videoclips(clips, method="compose")

    audio = AudioFileClip(f"{dir_name}/{name}.mp3")
    print(audio.duration)
    print(video_clip.duration)
    video_clip.audio = audio

    video_clip.write_videofile(
        f"{dir_name}/{name}.mp4",
        codec="libx264",
        audio=f"{dir_name}/{name}.mp3",
        fps=24,
        audio_codec="libmp3lame",
        audio_bitrate="48k",
    )

    vid = VideoFileClip(f"{dir_name}/{name}.mp4")
    print(vid)
    print(vid.audio)
