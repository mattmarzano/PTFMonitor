import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import sys
import threading
import time

from get_status import get_status

# fill out bot_token, app_token, channelid
bot_token = ""
app_token = ""
channelid = ""

app = App(token=bot_token)

def send_message(message):
    app.client.chat_postMessage(channel=channelid, text=message)

def monitor_status():

    laser_status_old, wiener_status_old = get_status()
    while True:
        
        laser_status, wiener_status = get_status()
        
        if laser_status != laser_status_old and laser_status != "Pend On":
            send_message(f"The laser has been turned {laser_status}")
            laser_status_old = laser_status
        if wiener_status != wiener_status_old and wiener_status != "Pend On":
            send_message(f"The HV has been turned {wiener_status}")
            wiener_status_old = wiener_status
        time.sleep(1)

monitor_thread = threading.Thread(target = monitor_status)
monitor_thread.daemon = True
monitor_thread.start()

@app.message("hello ptfmonitor")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>")

@app.message("ptfstatus")
def message_status(say):
    laser_status, wiener_status = get_status()
    say(f"The laser is {laser_status} and the HV is {wiener_status}")
        
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()