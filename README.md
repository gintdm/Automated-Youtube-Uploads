# Automated-Youtube-Uploads

Dependincies
Python v 3.x
and the following python libraries:
time, os, googleapiclient.discovery, configparser, pickle, requests, json, shutil, datetime, google_auth_oauthlib.flow, google.auth.transport.requests, googleapiclient.discovery, googleapiclient.http

Set-Up

1). To use the Uploader you must create 0Auth credentials for the Youtube account you wish to automate uploads for. 

you can visit https://developers.google.com/youtube/v3/getting-started for more information on 0Auth Tokens. 

you must save these credentials to the working directory as "my_secret.json"

2). You must create folders named "Waiting" and "Working" in your working directory. 

3). You must place a ".png" thumbnail with a name that matches the name of the coorosponding video into your working directory for each video. This will be that videos thumbnail.

4). You must populate the config file with the metadata you wish to add for your videos. 2 example config keys exist, "[key]" and "[test]"

5). Place the video you wish to upload into the "Waiting" folder and run main.py. 

