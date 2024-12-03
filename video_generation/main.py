import os
from dotenv import load_dotenv

load_dotenv()

from video_generation.images import generate_and_write_images_and_thumbnail
from video_generation.text_to_speech import convert_text_to_speech
from video_generation.video_maker import make_video
from video_generation.write_script import write_script


# from youtube_uploader import initialize_upload
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaFileUpload
# from google_auth_oauthlib.flow import InstalledAppFlow

# CLIENT_SECRETS_FILE = os.environ['CLIENT_SECRETS_FILE']
# SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
# API_SERVICE_NAME = 'youtube'
# API_VERSION = 'v3'
#
# VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')
#
# LANGUAGE = 'english'
# def get_authenticated_service():
#     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#     credentials = flow.run_local_server()
#     return build(API_SERVICE_NAME, API_VERSION, credentials=credentials, developerKey=os.environ['YOUTUBE_API_KEY'])


def generate_video(topic: str, length: int):
    base_dir = "."
    base_name = "".join(topic.split()).replace("'", "")
    dir_name = f"{base_dir}/{base_name}"
    name = "".join([i.capitalize() for i in topic.split()])
    if os.path.isdir(dir_name):
        print("Directory already exists!")
        return f"{dir_name}/{name}.mp4"
    os.mkdir(dir_name)
    script = write_script(topic, length, name, dir_name)
    print("Script written!\n", script)
    voice_length = convert_text_to_speech(path=dir_name, name=name, text=script)
    print("Voice generated! Duration: ", voice_length)
    n = generate_and_write_images_and_thumbnail(script, length, dir_name)
    if n > 0:
        return make_video(n, dir_name, voice_length, name)


# args = generate_args(
#     dir_name=dir_name, topic=detailed_topic, script=script, name=name
# )
# # initialize_upload(youtube, args)
# time.sleep(time_between_videos)
