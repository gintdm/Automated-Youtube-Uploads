import datetime
import os
import shutil
import configparser
from lib import *

# Read Configuration File
config = configparser.ConfigParser()
config.read('config.ini')

# File Management 
# a). moves contents of ./Waiting to ./Working &
# b). begins to upload contents one at a time. 

show_list = os.listdir(os.getcwd() + "\\Waiting")

# a). move contents of ./Waiting to ./Working
for index in show_list:

    shutil.move(os.getcwd() + "\\Waiting\\" + index, os.getcwd() + "\\Working\\" + index)

# b). Create variables and call upload function "auth()" for each element in show_list[] located in ./Working
for index in show_list:

    # Parse and format "index"
    index = (os.getcwd() + "\\Working\\" + index)
    filename = index.split(".")[0]
    filename = filename.split("_")[-1]

    # Date and Time variables
    realtime = datetime.datetime.now()
    year = realtime.strftime("%Y")
    realtime = realtime.strftime("%A %B %#d,")
    time_to_upload = config[filename]["time_to_upload"]

    # Youtube MetaData
    title = (realtime + " " + config[filename]["title"] + " - " + year)
    description = config[filename]["description"]
    tags = config[filename]["tags"]

    # Upload function "auth()"
    auth(index, title, description, tags, time_to_upload)