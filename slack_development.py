import os
import slack
def slack_notification(title)
client = slack.WebClient(token='xoxp-379481221041-908071910834-908318101362-eca592495a8903a7a08131effe559eca')

response = client.chat_postMessage(
    channel='#random',
    text="Hello world!")
assert response["ok"]
assert response["message"]["text"] == title, 'has completed uploading, please review, add endscreens to, and publish the video on Youtube'
