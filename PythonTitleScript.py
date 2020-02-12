import requests
import datetime
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

realtime = datetime.datetime.now()
timestamp = '1500'
date = realtime.strftime("%B %#d" + " " + "%Y")

title = config[timestamp]['title']
description = config[timestamp]['description'] + ", " + date
title = "SelectedName=Title&Value=" + title
description = "SelectedName=Description&Value=" + description
base_url = 'http://192.168.0.12:8088/api/?Function=SetText&Input=Title8AmericasBlue.xaml&'

title_url = ''.join([base_url, title])
description_url = ''.join([base_url, description])

requests.get(title_url)
requests.get(description_url)

requests.get('http://192.168.0.12:8088/api/?Function=OverlayInput1In&Input=Title8AmericasBlue.xaml&Fade=1150')

time.sleep(6)

requests.get('http://192.168.0.12:8088/api/?Function=OverlayInput1Out&Input=Title8AmericasBlue.xaml&Fade=1150')
