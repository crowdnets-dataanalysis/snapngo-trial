"""
terminal command to get into SQL: 
source .bash_profile
mysql -u root -p


to get slack running:
ngrok http 5000 (in one terminal)
run this file in another terminal
(both of these things need to happen in order to run )
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql

from slack_sdk import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError



# setting up .env path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# connecting to my (Sofia's) SQL database


# cur = conn.cursor()
# cur.execute("USE test1;")
# cur.execute("SELECT * FROM cats WHERE name = 'scotty';")
# output = cur.fetchall()
# print(output)


# cur.execute("USE test1;")
# cur.execute("SELECT colOne from first;")
# output = cur.fetchall()[0][0]



# create flask app
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['CAT_BOT_SIGNING_SECRET'], '/slack/events', app)

# sending a message to Slack
client = WebClient(token=os.environ['CAT_BOT_TOKEN'])
# client.chat_postMessage(channel='#bot-testing', text=f'From SQL database: {output}!')

@ slack_event_adapter.on('message')
def message(payload):
    print()
    print('NEW MESSAGE')
    print()
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    print('TEXT', text)

    

    if text == "hi":
        client.chat_postMessage(channel=channel_id,text="Meow! I'm a cat!")
    
    # elif 'cat' in text:
    #     print("--  cat in text!!")
    #     try:
    #         cat_id = [char for char in text if char.isdigit()][0]
    #         print(cat_id)

    #         conn = pymysql.connect(
    #         host='localhost',
    #         user='root',
    #         password=os.environ['SQL_PASS'],
    #         db='test1'
    #         )
    #         cur = conn.cursor()
    #         print(2)
    #         cur.execute("USE test1;")
    #         print(3)
    #         cur.execute("SELECT * FROM cats WHERE cat_id = 1;")
    #         print(4)
    #         cat_info = cur.fetchall()[0]
    #         conn.close()

    #         print(cat_info)
    #         response = client.files_upload_v2(
    #             file='/Users/skobayashi/Desktop/snap-n-go/snapngo/cat_pics/cat1.png',
    #             # initial_comment=f'cat',
    #             initial_comment=f'Behold {cat_info[0].title()}, cat #{cat_info[2]}!', 
    #             channels=channel_id
    #         )
    #     except SlackApiError as e:
    #         # You will get a SlackApiError if "ok" is False
    #         assert e.response["ok"] is False
    #         # str like 'invalid_auth', 'channel_not_found'
    #         assert e.response["error"]
    #         print(f"Got an error: {e.response['error']}")
    



if __name__ == "__main__":
    app.run(debug=True)
