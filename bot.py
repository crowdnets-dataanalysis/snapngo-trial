import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError

SLACK_TOKEN= "xoxb-5036818184306-5036936607890-F7yyWUVEDEdeyNQqIhKzjL8H"
SIGNING_SECRET="966031e0a648505527c75ee5ceefbfe8"

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app) 

client = slack.WebClient(token=SLACK_TOKEN)

@ slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')

    response = client.conversations_open(users=[user_id])
    dm_channel_id = response["channel"]["id"]
    if channel_id == dm_channel_id:
        handle_dm_message(payload)
    else:
        # Send a Direct Message to the user and ask if they want a task
        try:
            client.chat_postMessage(channel=channel_id, text="Hello! Check your DMs for further instructions")
            client.chat_postMessage(channel=dm_channel_id, text="Would you like a task? (yes or no)")
        except SlackApiError as e:
            print("Error: {}".format(e))

# Define the function to handle incoming messages in the Direct Message conversation
def handle_dm_message(event_data):
    dm_message = event_data["event"]
    dm_user_id = dm_message["user"]
    dm_text = dm_message.get("text", "").lower()
    response = client.conversations_open(users=[dm_user_id])
    dm_channel_id = response["channel"]["id"]
    # Check if the user wants a task
    if dm_text == "yes":
        tasks = ["Task 1", "Task 2", "Task 3"]
        task_list = "\n".join(["{}. {}".format(i+1, task) for i, task in enumerate(tasks)])
        try:
            # Send a Direct Message with the list of tasks
            client.chat_postMessage(channel=dm_channel_id, text="Here are your tasks:\n{}".format(task_list))
            client.chat_postMessage(channel=dm_channel_id, text="Please select one (1, 2, or 3)")

        except SlackApiError as e:
            print("Error: {}".format(e))

    # Otherwise, reprompt the user if they want a task
    elif dm_text == "no":
        try:
            client.chat_postMessage(channel=dm_channel_id, text="OK, if you change your mind, just send the message \"yes\" and I will reassign some tasks for you.")
        except SlackApiError as e:
            print("Error: {}".format(e))

    elif dm_text == "1":
        try:
            # Send a Direct Message with the selected task
            client.chat_postMessage(channel=dm_channel_id, text="You selected task 1. Once you recieve the message for submission, send me a message with just the image.")

        except SlackApiError as e:
            print("Error: {}".format(e))

    elif dm_text == "2":
        try:
            # Send a Direct Message with the selected task
            client.chat_postMessage(channel=dm_channel_id, text="You selected task 2. Once you recieve the message for submission, send me a message with just the image.")

        except SlackApiError as e:
            print("Error: {}".format(e))

    elif dm_text == "3":
        try:
            # Send a Direct Message with the selected task
            client.chat_postMessage(channel=dm_channel_id, text="You selected task 3. Once you recieve the message for submission, send me a message with just the image.")

        except SlackApiError as e:
            print("Error: {}".format(e))

    else:
        try:
            client.chat_postMessage(channel=dm_channel_id, text="I didn't understand. Please try again")
        except SlackApiError as e:
            print("Error: {}".format(e))


#def choice(event_data):
    
    
if __name__ == "__main__":
    app.run(debug=True)
