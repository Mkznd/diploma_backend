class TopicManager:
    def __init__(self, directory: str, topic: str):
        self.topic = topic
        self.dir = directory

    def get_full_list(self):
        with open(f"{self.dir}/{self.topic}_full_list.txt", "a+") as file:
            file.seek(0, 0)
            return [line.rstrip() for line in file if line != ""]

    def get_used_list(self):
        with open(f"{self.dir}/{self.topic}_used_list.txt", "a+") as file:
            file.seek(0, 0)
            return [line.rstrip() for line in file if line != ""]

    def get_unused_list(self):
        with open(f"{self.dir}/{self.topic}_unused_list.txt", "a+") as file:
            file.seek(0, 0)
            return [line.rstrip() for line in file if line != ""]

    def add_full_list(self, topic: str):
        with open(f"{self.dir}/{self.topic}_full_list.txt", "a+") as file:
            file.write(topic + "\n")

    def add_used_list(self, topic: str):
        with open(f"{self.dir}/{self.topic}_used_list.txt", "a+") as file:
            file.write(topic + "\n")

    def add_unused_list(self, topic: str):
        with open(f"{self.dir}/{self.topic}_unused_list.txt", "a+") as file:
            file.write(topic + "\n")

    def remove_from_full_list(self, topic: str):
        a = self.get_full_list()
        with open(f"{self.dir}/{self.topic}_full_list.txt", "w") as file:
            if topic in a:
                a.remove(topic)
                file.write("\n".join(a))

    def remove_from_used_list(self, topic: str):
        a = self.get_used_list()
        with open(f"{self.dir}/{self.topic}_used_list.txt", "w") as file:
            a.remove(topic)
            file.write("\n".join(a))

    def remove_from_unused_list(self, topic: str):
        a = self.get_unused_list()
        with open(f"{self.dir}/{self.topic}_unused_list.txt", "w") as file:
            a.remove(topic)
            file.write("\n".join(a))

    def clear_full_list(self):
        with open(f"{self.dir}/{self.topic}_full_list.txt", "w"):
            pass

    def clear_used_list(self):
        with open(f"{self.dir}/{self.topic}_used_list.txt", "w"):
            pass

    def clear_unused_list(self):
        with open(f"{self.dir}/{self.topic}_unused_list.txt", "w"):
            pass

    def add_topic(self, topic: str):
        self.add_full_list(topic)
        self.add_unused_list(topic)

    def add_topics(self, topics: list):
        for topic in topics:
            self.add_topic(topic)

    def use_topic(self, topic: str):
        self.remove_from_unused_list(topic)
        self.add_used_list(topic)

    def remove_topic(self, topic: str):
        self.remove_from_full_list(topic)
        self.remove_from_used_list(topic)
        self.remove_from_unused_list(topic)
