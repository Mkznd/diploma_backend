from dotenv import load_dotenv
from completions.completions import text_to_speech
from mutagen.mp3 import MP3

load_dotenv()


def convert_text_to_speech(path: str, name: str, text: str):
    response = text_to_speech(text)
    response.write_to_file(f"{path}/{name}.mp3")
    f = MP3(f"{path}/{name}.mp3")
    return f.info.length
