# Automated-Youtube-Uploads

Dependincies
Python v 3.x

import time
import os
import googleapiclient.discovery
import configparser
import pickle
import requests
import glob
import json
import shutil

import datetime
import os
import shutil
import configparser
from lib import *

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


Set-Up

1). To use the Uploader you must create 0Auth credentials for the Youtube account you wish to automate uploads for. 

you can visit https://developers.google.com/youtube/v3/getting-started for more information on 0Auth Tokens. 

you must save these credentials to the working directory as "my_secret.json"


