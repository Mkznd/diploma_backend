def get_topic_prompt(topic):
    return """Write a list of 10 short topics for an educational YouTube videos about {} separated by newline. 
    Don't enumerate them in any way, just write topics""".format(
        topic
    )
