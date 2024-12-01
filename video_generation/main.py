import os
import time

from openai import OpenAI

from completions.completions import generate_topics
from images import generate_and_write_images_and_thumbnail
from text_to_speech import convert_text_to_speech
from topic_manager import TopicManager
from video_maker import make_video
from write_script import write_script

from youtube_args_generator import options, generate_args

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

base_dir = "."
topic = input("The topic for the video: ").title()
length = int(input("The length of the video: "))
base_name = "".join(topic.split()).replace("'", "")
ideas_dir = f"{base_dir}/ideas"
if not os.path.isdir(ideas_dir):
    os.mkdir(ideas_dir)
topic_manager = TopicManager(ideas_dir, topic)
time_between_videos = 0
# youtube = get_authenticated_service()

topic_dir = f"{base_dir}/{topic}"
if not os.path.isdir(topic_dir):
    os.mkdir(topic_dir)

# while True:
unused_topics = topic_manager.get_unused_list()
if len(unused_topics) == 0:
    generated_topics = [
        i for i in generate_topics(topic) if i not in topic_manager.get_used_list()
    ]
    topic_manager.add_topics(generated_topics)
    unused_topics = topic_manager.get_unused_list()

detailed_topic = unused_topics[0]
name = "".join([i.capitalize() for i in detailed_topic.split()])
dir_name = f"{topic_dir}/{name}"
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)
script = write_script(detailed_topic, length, name, dir_name)
voice_length = convert_text_to_speech(path=dir_name, name=name, text=script)
print("Voice generated! Duration: ", voice_length)
n = generate_and_write_images_and_thumbnail(script, length, dir_name)
if n > 0:
    make_video(n, dir_name, voice_length, name)
topic_manager.use_topic(detailed_topic)
# args = generate_args(
#     dir_name=dir_name, topic=detailed_topic, script=script, name=name
# )
# # initialize_upload(youtube, args)
# time.sleep(time_between_videos)
