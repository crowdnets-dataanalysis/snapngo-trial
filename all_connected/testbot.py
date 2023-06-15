import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql
import json
import requests
import messenger

from slack_sdk import WebClient
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler


env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("CAT_BOT_TOKEN"),
    # signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)

# Initialize Flask app
flask_app = Flask(__name__)

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
handler = SlackRequestHandler(app)

# Register routes to Flask app
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)

slack_event_adapter = SlackEventAdapter(os.environ['CAT_BOT_SIGNING_SECRET'], '/slack/events', flask_app)

# Define the client obj
client = WebClient(token=os.environ['CAT_BOT_TOKEN'])
# Get the bot id
BOT_ID = client.api_call("auth.test")['user_id']

def getAllUsersInfo():
    '''
    Helper function to get all users info from slack
    Takes a users array we get from slack which is a SlackResponse object type
    Returns a dict type containing same info with user id as key
    '''
    # Call the users.list method using the WebClient
    # users.list requires the users:read scope
    result = client.users_list()
    # Get all user info in result
    users_array = result["members"]
    users_store = {}
    # turn the SlackResponse object type into dict type
    for user in users_array:
        # Key user info on their unique user ID
        user_id = user["id"]
        # Store the entire user object (you may not need all of the info)
        users_store[user_id] = user
    return users_store

def generateMessage(assignList):
    '''
    Helper function for sendTasks.
    Get the list of task assigned to a user and format them into a 
    json block message.
    Return the block message
    '''
    block = []
    for taskInfo in assignList:
        text = ("Task" + str(taskInfo[0]) + " Location: " + taskInfo[2] + 
                "\nDescription: " + taskInfo[3] + 
                "\nStart time: " + str(taskInfo[4]) + " Window: " + str(taskInfo[5])+ 
                "\nCompensation: " + str(taskInfo[6]))
        block.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        )
        block.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Accept",
                        },
                        "value": "accepted",
                        "action_id": "accepted"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject",
                        },
                        "value": "rejected",
                        "action_id": "rejected"
                    }
                ],
                "block_id": str(taskInfo[0])
            }
        )
    return block

def sendTasks(assignmentsDict):
    '''
    * Message users to give them new tasks *
    Takes the assignments dictionary generated by getAssignments() in messenger
    Format the tasks each user get into block messages. Send them to each 
        user respectively
    Returns nothing
    ''' 
    for user_id in assignmentsDict:
        if BOT_ID != user_id:    
            try:
                reply = generateMessage(assignmentsDict[user_id])
                texts = "Here are your newly generated tasks"
                client.chat_postMessage(channel=f"@{user_id}", text = texts, blocks = reply)
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                # str like 'invalid_auth', 'channel_not_found'
                assert e.response["error"]
                print(f"Got an error: {e.response['error']}")

@app.message()
def any_message(payload, say):
    """
    Takes the response from a message sent in any chat in which this Bot has
        access to.
    When on, constantly listens for new messages, the responds as dictated below.
    Returns nothing.
    """
    # Recieve payload
    print(payload)
    channel_id = payload.get('channel')
    user_id = payload.get('user')
    text = payload.get('text')
    #print(f'\nUSER_ID: {user_id}\n')
    
    # Handle certain responses
    if BOT_ID != user_id:
        return #needs to be changed

def getPic(url, token, user_id, task_id):
    '''
    Takes   url: from payload['event']['files'][0]['url_private_download']
            token: the bot token
            user_id: the user who sent the picture
            task_id: the task they are trying to finish, should be payload['event']['text']
    Downloads picture with the given download url and saves it in the given path
    '''
    r = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
    dateTime = 0 # switch to clock
    filename = f"../../snapngo_pics/{user_id}_{task_id}_{dateTime}.jpeg"
    open(filename, 'wb').write(r.content)


@app.action("accepted")
def action_button_click(body, ack, say):
    '''
    body['actions'][0]   {'value': 'accepted', 'block_id': '1', 'type': 'button', 'action_id': 'accepted', 'text':...}
    '''
    # Acknowledge the action
    ack()
    action = body['actions'][0]
    status = action['value']
    task = int(action['block_id'])
    user = str(body['user']['id'])
    messenger.updateAssignStatus(status, task, user)
    say(f"<@{body['user']['id']}> accepted task {body['actions'][0]['block_id']}")
    

@app.action("rejected")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    action = body['actions'][0]
    status = action['value']
    task = int(action['block_id'])
    user = str(body['user']['id'])
    messenger.updateAssignStatus(status, task, user)
    say(f"<@{body['user']['id']}> rejected task {body['actions'][0]['block_id']}")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()