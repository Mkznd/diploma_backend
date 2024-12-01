from video_generation.completions.completions import generate_script


def write_script(topic: str, length: int, name: str, dir_name: str):
    script = generate_script(topic, length)

    f = open(f"{dir_name}/{name}.txt", "w")
    f.write(script)
    f.close()
    print(f"Script written!\n{script}")
    return script
