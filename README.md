# Automated-Youtube-Uploads

Dependincies
Python v 3.x
and the following python modules, easily installed with pip
time, os, googleapiclient.discovery, configparser, pickle, requests, json, shutil, datetime

+

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


Set-Up

1). To use the Uploader you must create 0Auth credentials for the Youtube account you wish to automate uploads for. 

you can visit https://developers.google.com/youtube/v3/getting-started for more information on 0Auth Tokens. 

you must save these credentials to the working directory as "my_secret.json"

2). You must create folders named "Waiting" and "Working" in your working directory. 

3). You must place a ".png" thumbnail with a name that matches the name of the coorosponding video into your working directory for each video. This will be that videos thumbnail.

4). Place the Video you wish to upload into the waiting folder and run main.py. 

