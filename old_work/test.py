import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Set the API token and signing secret
app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# Define the function to handle incoming messages in the channel
@app.event("message")
def handle_message(event, say):
    user_id = event["user"]
    text = event.get("text", "").lower()
    channel_id = event["channel"]

    # Send a Direct Message to the user and ask if they want a task
    try:
        response = client.conversations_open(users=[user_id])
        dm_channel_id = response["channel"]["id"]
        client.chat_postMessage(channel=dm_channel_id, text="Do you want a task?")
    except SlackApiError as e:
        print("Error: {}".format(e))

    # Define the function to handle incoming messages in the Direct Message conversation
    @app.event("message")
    def handle_dm_message(event, say):
        dm_user_id = event["user"]
        dm_text = event.get("text", "").lower()

        # Check if the user wants a task
        if dm_text == "yes":
            tasks = ["Task 1", "Task 2", "Task 3"]
            task_list = "\n".join(["{}. {}".format(i+1, task) for i, task in enumerate(tasks)])
            try:
                # Send a Direct Message with the list of tasks
                client.chat_postMessage(channel=dm_channel_id, text="Here are your tasks:\n{}".format(task_list))
            except SlackApiError as e:
                print("Error: {}".format(e))

        # Otherwise, reprompt the user if they want a task
        elif dm_text == "no":
            try:
                client.chat_postMessage(channel=dm_channel_id, text="OK, let me know if you change your mind.")
            except SlackApiError as e:
                print("Error: {}".format(e))
        else:
            try:
                client.chat_postMessage(channel=dm_channel_id, text="I didn't understand. Do you want a task?")
            except SlackApiError as e:
                print("Error: {}".format(e))

    # Set the context of the Direct Message conversation
    say("I've sent you a Direct Message with a question. Please check your Direct Messages.")

if __name__ == "__main__":
    handler = SocketModeHandler(app_token=os.environ["SLACK_APP_TOKEN"])
    handler.start() 