def get_prompt_for_script(topic, length):
    return """Write a narrator text of a script for an education Youtube video explaining {} for general audience with intro and outro 
    make it around {} words""".format(
        topic.capitalize(), length * 150
    )


def get_improvement_prompt(text, length):
    return """Make the following text better and correct any mistakes, be it grammatical or stylistic.
    remove the labels for intro, main part, outro if they are present in the text:
    {}
    make it around {} words""".format(
        text, length * 150
    )
