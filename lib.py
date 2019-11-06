# Library
# A Library of Classes, Methods, and Functions for use by the Automated Youtube Uploader 

import time
import os
import googleapiclient.discovery
import configparser
import pickle
import requests
import glob
import json
import shutil

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def auth(filename, title, description, tags, time_to_upload):

# Format the given filename from its given form. 
    my_parsed_target = filename.split('/')[-1]
    my_thumbnail_dst = my_parsed_target.split(".")[0]
  
# Format the time_to_upload from its "seconds since epoch"  form 
    time_to_upload = float(time_to_upload)
    estimated_upload_time = time.time() + time_to_upload
    estimated_upload_time = time.ctime(estimated_upload_time)

# Create variables for the 0Auth process. 
    api_service_name = "youtube"
    api_version = "v3"
    scopes = ["https://www.googleapis.com/auth/youtube"]
    creds = None

# Authentication Example from https://developers.google.com/drive/activity/v1/quickstart/python "Step 3: Set up the sample"
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

# Build the API 
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    print("Youtube Uploader - Uploading " + title +
          "...    The Estimated Completion time is " + estimated_upload_time)

# Build Upload Call
    upload = youtube.videos().insert(  
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "27",
                "description": description,
                "title": title,
                "tags": tags
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(
           os.getcwd() +"\\Working\\" + filename.split("\\")[-1], chunksize=5120*1024, resumable=True)
    )
    
# Logic for resumable uploads
    while upload is None:
        upload = upload.next_chunk()

        if "id" in upload:
            print('Youtube Uploader - ' + title +
                  " was uploaded to Youtube succesfully")

# Execution of Upload Call
    video_id = json.loads(json.dumps(upload.execute())).get(
        'id')

# Build the Thumbnail call
    change_thumbnail = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(os.getcwd() + filename.split("\\")[-1].split(".")[0] + ".png"
                                   )
    )

# Call the Thumbnail update
    change_thumbnail.execute()
