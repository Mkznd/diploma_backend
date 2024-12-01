def get_images_prompt(script: str, number: int):
    text = """Using descriptive language, write descriptions of {} photorealistic pictures that are going to be a part of slideshow for the following script:
    {}
    Don't enumerate them in any way. Just write the prompts delimited by new lines. Avoid using descriptions of people and animals if possible. Example format:
    A shimmering galaxy cluster surrounded by a veil of twinkling stars, highlighting the invisible forces of dark matter that bind it together.
    A darkened underground laboratory filled with intricate scientific equipment, capturing the essence of the hunt for elusive dark matter particles.
    etc.""".format(
        number, script
    )
    return text


def get_thumbnail_prompt(script: str):
    return """Using descriptive language, write description for a thumbnail picture for the following script cript {}
    Don't write anything else. Just write the prompt.""".format(
        script
    )
