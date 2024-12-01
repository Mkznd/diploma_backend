from openai import OpenAI
from dotenv import load_dotenv
from openai._legacy_response import HttpxBinaryResponseContent

from completions.image_prompts import get_images_prompt, get_thumbnail_prompt
from completions.script_prompts import get_prompt_for_script, get_improvement_prompt
from completions.topic_prompts import get_topic_prompt
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

client = OpenAI()


def generate_topics(topic: str):
    response = prompt_as_assistant(get_topic_prompt(topic))
    return [i.strip() for i in response.split("\n")]


def generate_script(topic: str, length: int):
    script = prompt_as_assistant(get_prompt_for_script(topic, length))
    improved_script = prompt_as_assistant(get_improvement_prompt(script, length))
    return improved_script


def text_to_speech(text: str) -> HttpxBinaryResponseContent:
    return client.audio.speech.create(model="tts-1", voice="alloy", input=text)


def generate_image(prompt: str):
    return client.images.generate(prompt=prompt, n=1, size="1024x1024").data[0].url


def generate_images(script: str, number: int) -> list[str]:
    prompts = [
        i.strip()
        for i in prompt_as_assistant(get_images_prompt(script, number)).split("\n")
        if i
    ]
    print(prompts)
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(generate_image, i) for i in prompts]
    return [task.result() for task in running_tasks]


def generate_thumbnail(script: str) -> str:
    return generate_image(get_thumbnail_prompt(script))


def prompt_as_assistant(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a creative assistant, who helps me with creating youtube videos. Write only the "
                "answer to a question, nothing more",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content
