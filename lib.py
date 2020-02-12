# Library
# A Library of Classes, Methods, and Functions for use by the Youtube Uploader and Post-Production GUIs
# archive(), change_playlist(), change_thumbnail()

import time
import os
import googleapiclient.discovery
import configparser
import pickle
import requests
import glob
import json
import shutil
import slack

from tkinter import filedialog
from moviepy.editor import *
from tqdm import tqdm
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def slack_notification(title):
    
    client = slack.WebClient(token='xoxp-379481221041-908071910834-908318101362-eca592495a8903a7a08131effe559eca')

    response = client.chat_postMessage(
    channel='UB6SZHBHC',
    text=title + ' has completed uploading, please review, add endscreens to, and publish the video on Youtube'
)
    assert response["ok"]
    assert response["message"]["text"] == title + ' has completed uploading, please review, add endscreens to, and publish the video on Youtube'



def produce(my_target, thumbnail, end_screen, rip_audio):

    my_parsed_target = str(my_target.split('\\')[-1])
    my_thumbnail_dst = my_parsed_target.split(".")[0]
    filename = my_target
    if rip_audio == "True":
        # Get Video and Image Rescources
        my_clip = VideoFileClip(my_parsed_target, audio=True).subclip(0, -21)
        end_clip = VideoFileClip(my_parsed_target, audio=True).subclip(-20)
        shrink_clip = VideoFileClip(
            my_parsed_target, audio=True).subclip(-21, -20)

        end_screen = ImageClip("end.png").set_duration(1)
        end_screen2 = ImageClip("end.png").set_duration(20)

        imgpath = (os.getcwd() + "\\" + ('{}.png'.format(filename.split("\\")[-1].split(".")[0])))

        # Concatenate and Composite resources to create produce_clip
        final_clip = CompositeVideoClip(
            [end_screen, shrink_clip.resize(lambda t: 1-.5*t)])
        final_end_clip = CompositeVideoClip([end_screen2, end_clip.resize(.5)])
        produce_clip = concatenate_videoclips(
            [my_clip, final_clip.resize(my_clip.size), final_end_clip.resize(my_clip.size)])

        # Create Audio Object
        audio_clip = produce_clip.audio

        # Write thumbnail to destination
        thumbnail = my_clip.save_frame(imgpath, thumbnail)

        # Write Audio to destination
        audio_clip.write_audiofile(
            my_thumbnail_dst + ".wav", fps=44100, nbytes=2, bitrate="128k")

        # Write produce_clip to destination
        produce_clip.write_videofile("my_clip.mp4", preset="ultrafast")

    elif end_screen == "True":
        # Get Video and Image Rescources
        my_clip = VideoFileClip(
            my_parsed_target, audio=True).subclip(0, -21)
        end_clip = VideoFileClip(my_parsed_target, audio=True).subclip(-20)
        shrink_clip = VideoFileClip(
            my_parsed_target, audio=True).subclip(-21, -20)

        end_screen = ImageClip("end.png").set_duration(1).resize(my_clip.size)
        end_screen2 = ImageClip("end.png").set_duration(
            20).resize(my_clip.size)

        imgpath = (os.getcwd() + "\\" + ('{}.png'.format(filename.split("\\")[-1].split(".")[0])))


        # Concatenate and Composite resources to create produce_clip
        final_clip = CompositeVideoClip(
            [end_screen, shrink_clip.resize(lambda t: 1-.5*t)])
        final_end_clip = CompositeVideoClip(
            [end_screen2, end_clip.resize(.5)])
        produce_clip = concatenate_videoclips(
            [my_clip, final_clip.resize(my_clip.size), final_end_clip.resize(my_clip.size)])

        # Write thumbnail to destination
        thumbnail = my_clip.save_frame(imgpath, thumbnail)

        # Write produce_clip to destination
        produce_clip.write_videofile(
            "my_clip.mp4", preset="ultrafast")

    else:
        os.rename(my_parsed_target, "my_clip.mp4")
        my_clip = VideoFileClip(
            "my_clip.mp4", audio=True).subclip(0, thumbnail)
        
        imgpath = (os.getcwd() + "\\" + ('{}.png'.format(filename.split("\\")[-1].split(".")[0])))

        thumbnail = my_clip.save_frame(imgpath, thumbnail)
        


def auth(filename, title, description, tags, playlist, phase, update_playlist, time_to_upload, realtime, year):

    my_parsed_target = filename.split('/')[-1]
    my_thumbnail_dst = my_parsed_target.split(".")[0]
    config = configparser.ConfigParser()
    date_config = configparser.ConfigParser()
    config.read('config.ini')
    date_config.read('date.ini')

    time_to_upload = float(time_to_upload)
    estimated_upload_time = time.time() + time_to_upload
    estimated_upload_time = time.ctime(estimated_upload_time)

    api_service_name = "youtube"
    api_version = "v3"
    scopes = ["https://www.googleapis.com/auth/youtube"]
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'my_secret.json', scopes)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    print("Youtube Uploader - Uploading " + title +
          "...    The Estimated Completion time is " + estimated_upload_time)

    upload = youtube.videos().insert(  # Build Upload Call
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "27",
                "description": description,
                "title": title,
                "tags": [tags]
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(
           filename.split("\\")[-1] + "\\my_clip.mp4", chunksize=5120*1024, resumable=True)
    )
    while upload is None:
        upload = upload.next_chunk()

        if "id" in upload:
            print('Youtube Uploader - ' + title +
                  " was uploaded to Youtube succesfully")

    video_id = json.loads(json.dumps(upload.execute())).get(
        'id')

    change_thumbnail = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(my_thumbnail_dst + ".png"
                                   )
    )

    # change_playlist = youtube.playlistItems().insert(
    #         part="snippet",
    #         body={
    #             "snippet": {
    #                 "playlistId": playlist,
    #                 "resourceId": {
    #                     "kind": "youtube#video",
    #                     "videoId": video_id
    #                 }
    #             }
    #         }
    #     )

    # get_id = youtube.playlistItems().list(
    #     part="id",
    #     maxResults=1,
    #     playlistId="PLDI7nZkS6noiSQxOrzD29tmcD_oyUeu3B"
    # )

    # delete_playlist_item = youtube.playlistItems().delete(id=get_id.execute())

    if playlist == "PLDI7nZkS6noiSQxOrzD29tmcD_oyUeu3B" and title == "NOON Market Update on TFNN":
        change_thumbnail.execute()

    elif playlist == "PLDI7nZkS6noiSQxOrzD29tmcD_oyUeu3B":
        change_thumbnail.execute()

    else:
        change_thumbnail.execute()
