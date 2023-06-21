import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import local_messenger
import json

from slack_sdk import WebClient
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from datetime import date


env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
token = os.environ.get("CAT_BOT_TOKEN")
# Initializes your app with your bot token and socket mode handler
app = App(
    token= token,
    # signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)


flask_app = Flask(__name__)

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
handler = SlackRequestHandler(app)

f = open('block_messages/help_block.json')
info_page = json.load(f)
f = open('block_messages/sample_task.json')
sample_task = json.load(f)

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

db_name = 'test1'
assign_dict = local_messenger.get_assignments(db_name)



def generate_message(task_info, user_id):
    '''
    Helper function for sendTasks.
    Get the list of task assigned to a user and format them into a 
    json block message.
    Return the block message
    '''
    block = []
    text = (f"""Task # {task_info[0]} \nLocation: {task_info[2]} \n
            Description: {task_info[3]}\n Start Time: {task_info[4]} \n
            Window: {task_info[5]} \n Compensation: {task_info[6]}""")

    description = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
    }
    buttons = _get_assign_status(task_info[0], user_id)
    block.append(description)
    block.append(buttons)
    return block

def _get_assign_status(task_id, user_id):
    status = local_messenger.get_assign_status(task_id, user_id)
    if status == "rejected":
        block = {     
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
                    "style": "danger",
                    "value": "rejected",
                    "action_id": "rejected"
                }                    
            ],
            "block_id": str(task_id)
        }
        
    elif status == "accepted":
        block = {     
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Accept",
                    },
                    "style": "primary",
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
            "block_id": str(task_id)
        }
    else:
        block = {     
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
            "block_id": str(task_id)
        }
    return block

def send_tasks(assignments_dict):
    '''
    * Message users to give them new tasks *
    Takes the assignments dictionary generated by getAssignments() in messenger
    Format the tasks each user get into block messages. Send them to each 
        user respectively
    Returns nothing
    ''' 
    for user_id in assignments_dict:
        if BOT_ID != user_id:   
            try:
                for task_info in assignments_dict[user_id]:
                    block = generate_message(task_info, user_id)
                    #texts = "Here are your newly generated tasks"
                    client.chat_postMessage(channel=f"@{user_id}", blocks = block)
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                # str like 'invalid_auth', 'channel_not_found'
                assert e.response["error"]
                print(f"Got an error: {e.response['error']}")

send_tasks(assign_dict)
local_messenger.update_assign_status("pending", 0, 0)


def get_all_users_info():
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




@app.message()
def handle_message(payload, say):
    """
    Takes the response from a message sent in any chat in which this Bot has
        access to.
    When on, constantly listens for new messages, the responds as dictated below.
    Returns nothing.
    """
    # Recieve payload
    print("MESSAGE")
    #print(payload)
    channel_id = payload.get('channel')
    user_id = payload.get('user')
    text = payload.get('text')
    #print(f'\nUSER_ID: {user_id}\n')
    # Handle certain responses
    if BOT_ID != user_id:
        if 'files' not in payload:
            if text.strip() == "?":
                say(info_page)
            else:          #user only sends text without attaching an image
                say(sample_task)
        else:
            print("text+img")
            if len(payload['files']) > 1: #user attaches more than one image
                say("You are attaching more than one file.")
                say(info_page)
                return
            file = payload['files'][0]
            if "image" not in file['mimetype']: #user attaches a file that is not an image
                say("The file you attached is not an image.")
                say(info_page)
                return
            task_id = int(payload['text'])
            say(f"<@{user_id}> is trying to finish task {task_id}")
            task_list = local_messenger.get_assigned_tasks(user_id)
            if task_id not in task_list: #the text the user enters isn't any of their assigned task numbers
                say(f"You were not assigned to task {task_id}")
                say(f"Your assigned tasks are {task_list}")
                return
            else:
                url = file['url_private_download']
                path = get_pic(url, token, user_id, task_id)
                if local_messenger.submit_task(user_id, task_id, path):
                    say(f"<@{user_id}> finished task {task_id}")
                else:
                    say(f'''Task {task_id} has already expired. 
                            Please pick another assigned task to finish.''')

            #update database if image is NULL
        return #needs to be changed

@app.event("message")
def handle_message_events(body, logger):
    '''
    When user only send a picture without text
    '''
    logger.info(body)
    user = body['event']['user']
    client.chat_postMessage(channel=f"@{user}",text= "SAMPLE TASK")


@app.event("file_shared")
def handle_file_shared_events():
    '''
    Don't need this. Just added it so we don't get warning messages from it.
    '''
    return

def get_pic(url, token, user_id, task_id):
    '''
    Takes   url: from payload['event']['files'][0]['url_private_download']
            token: the bot token
            user_id: the user who sent the picture
            task_id: the task they are trying to finish, should be payload['event']['text']
    Downloads picture with the given download url and saves it in the given path
    '''
    r = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
    date = date.today() # change to clock
    filename = f"../../snapngo_pics/{user_id}_{task_id}_{date}.jpeg"
    open(filename, 'wb').write(r.content)
    return filename


@app.action("accepted")
def action_button_click(body, ack, say):
    '''
    body['actions'][0]   {'value': 'accepted', 'block_id': '1', 'type': 'button', 'action_id': 'accepted', 'text':...}
    '''
    # Acknowledge the action
    ack()
    print("BUTTON CLICK")
    # print(local_messenger.assignment_objs.keys())
    # print(local_messenger.assignment_objs)
    action = body['actions'][0]
    new_status = action['value']
    task = int(action['block_id'])
    user = str(body['user']['id'])
    task_list = local_messenger.get_task_list(user, task)
    old_status = local_messenger.get_assign_status(task, user)
    if old_status == "pending":
        local_messenger.update_assign_status(new_status, task, user)
        # task_list = local_messenger.get
        message = generate_message(task_list, user)
        client.chat_update(channel=body["channel"]["id"], ts = body["message"]["ts"], blocks = message)
        say(f"<@{user}> {new_status} task {task}")
    else:
        say(f"<@{user}> already {old_status} task {task}")
    return
    

@app.action("rejected")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    print("BUTTON CLICK")
    # print(assignment_objs.keys())
    # print(assignment_objs)
    action = body['actions'][0]
    new_status = action['value']
    task = int(action['block_id'])
    user = str(body['user']['id'])
    # print(assignment_objs)
    task_list = local_messenger.get_task_list(user, task)
    old_status = local_messenger.get_assign_status(task, user)
    if old_status == "pending":
        local_messenger.update_assign_status(new_status, task, user)
        # task_list = local_messenger.get
        message = generate_message(task_list, user)
        client.chat_update(channel=body["channel"]["id"], ts = body["message"]["ts"], blocks = message)
        say(f"<@{user}> {new_status} task {task}")
    else:
        say(f"<@{user}> already {old_status} task {task}")
    return

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    #flask_app.run(debug=True)