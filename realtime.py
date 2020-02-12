import datetime
import os
import shutil
import configparser
import time
from lib import *

config = configparser.ConfigParser()
config.read('config.ini')
newscasts = ['0859.mp4','0900.mp4','9AM.mp4','0959.mp4','1000.mp4','XAM.mp4','1159.mp4','1200.mp4','XII.mp4','NOON.mp4','1259.mp4','0100.mp4','1PM.mp4','0159.mp4','0200.mp4','2PM.mp4','0259.mp4','0300.mp4','3PM.mp4','0359.mp4','0400.mp4','4PM.mp4','0307.mp4','DMR.mp4']
#file management
show_list = os.listdir(os.getcwd() + "\\Waiting")

for index in show_list:
    if index.split("_")[0] == "SyncToy":
        show_list.remove(index)
        
for index in show_list:
    if index == "logs":
        show_list.remove(index)

for index in show_list:
    if index.split(".")[-1] == "tmp":
        show_list.remove(index)


intersection_list = [value for value in show_list if value.split('_')[-1] in newscasts]

for index in intersection_list:
    show_list.insert(0, show_list.pop(show_list.index(index)))


for index in show_list:
    shutil.move(os.getcwd() + "\\Waiting\\" + index, os.getcwd() + "\\Working\\" + index)



for index in show_list:
    index = (os.getcwd() + "\\Working\\" + index)

    #date variables
    realtime = datetime.datetime.now()
    year = realtime.strftime("%Y")
    day_suffix = realtime.strftime("%#d")
    realtime = realtime.strftime("%B %#d")

    #Youtube MetaData
    filename = index.split(".")[0]
    filename = filename.split("_")[-1]
    try:
        title = (realtime + config["DAYS"][day_suffix] + " " + config[filename]["title"] + " - " + year)
    except:
        filename = index.split("\\")[-1]
        filename = filename.split(".")[0]
        filename = filename.split("_")[0]
        title = (realtime + config["DAYS"][day_suffix] + " " + config[filename]["title"] + " - " + year)
    
    description = config[filename]["description"]
    tags = config[filename]["tags"]

    #upload parameters
    playlist = config[filename]["playlist"]
    phase = "phase7"
    update_playlist = config[filename]["update_playlist"]
    time_to_upload = config[filename]["time_to_upload"]

    #production parameters
    rip_audio = config[filename]["rip_audio"]
    end_screen = config[filename]["end_screen"]
    thumbnail = int(config[filename]["thumbnail"])
   
    wrking_dir = os.getcwd()
    new_dir = os.getcwd() + "\\" + index.split("\\")[-1].split(".")[0]
    path = new_dir 
    
    try:
        os.mkdir(new_dir)
    except:
        shutil.rmtree(new_dir)
        os.mkdir(new_dir)

    source = index
    destination = new_dir
    shutil.move(source, destination)
    shutil.copy(os.getcwd() + "\\end.png", new_dir)
    os.chdir(path)
    produce(index, thumbnail, end_screen, rip_audio)
    index = os.getcwd() + "\\" + index.split("\\")[-1].split(".")[0]
    path = wrking_dir
    os.chdir(path)
    auth(index, title, description, tags, playlist, phase, update_playlist, time_to_upload, realtime, year)
    slack_notification(title)
    shutil.copytree(destination, os.getcwd()  + "//Produced Content//" + title)
    