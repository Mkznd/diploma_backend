import os

import openai

from dotenv import load_dotenv

load_dotenv()


class options:
    def __init__(self, file, title, privacyStatus, keywords=None, description='Test Description', category='27',
                 thumbnail=None):
        self.thumbnail = thumbnail
        self.category = category
        self.description = description
        self.keywords = keywords
        self.privacyStatus = privacyStatus
        self.title = title
        self.file = file


def generate_description(topic):
    return """Write a description for an education Youtube video with the following script:\n{}""".format(
        topic
    )


def generate_tags(script):
    return """Look for some keywords in the following script and write them separated by a whitespace:\n{}""".format(
        script
    )


openai.api_key = os.environ['OPENAI_API_KEY']


def generate_args(topic: str, script: str, name: str, dir_name: str):
    args = options(file=f'{dir_name}/{name}.mp4', title=topic, privacyStatus='public')
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_description(script),
        temperature=0.6,
        max_tokens=2048
    )
    description = response["choices"][0]["text"]
    # description = "test desc"
    args.description = description
    args.thumbnail = f'{dir_name}/{name}/photos/thumbnail.png'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_tags(script),
        temperature=0.6,
        max_tokens=2048
    )
    args.keywords = response["choices"][0]["text"].split()
    return args
