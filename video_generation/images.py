import os
import re
from math import ceil
import requests

import openai
from dotenv import load_dotenv

from video_generation.completions.completions import generate_images, generate_thumbnail

load_dotenv()


def generate_and_write_images_and_thumbnail(script: str, length: int, dir_name: str):
    number = ceil(length * 3)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    if not os.path.isdir(f"{dir_name}/images"):
        os.mkdir(f"{dir_name}/images")
    image_urls = generate_images(script, number)
    for i, url in enumerate(image_urls):
        image = requests.get(url)
        with open(f"{dir_name}/images/{i}.png", "wb") as file:
            file.write(image.content)
    print("Images generated!")
    return len(image_urls)
