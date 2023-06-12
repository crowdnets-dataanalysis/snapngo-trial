## Snap N Go 
##### by the Summer 2023 Lab (Sofia Kobayashi & Helen Mao)

### File System
- `all_connected/` directory is where all the final components and their backend driver (`connections.py`) are stored.
- `old_work/` is where we put previous students' work to reference and to make sure none of it got overwritten.
- `cat_bot` holds our Summer '23 test bot named catBot. Sometimes, it sends cat pics to the Slack. It also has some notes & examples on how to:
  1. Send messages from the Bot -> Slack (prompted by running the `sending_slack_messages.py` file)
  2. Connect to a web server & SQL server to listen for user messages & send back automatic responses (in the `cat_bot.py` file)
<br>

### Steps to Get Slack Bot Running on a Web Server (aka Automatically Responding to User Messages):
* Assumes you have all auto-response code ready & just need to connect to a server
1. Follow [this tutorial](https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/), starts around step 20

- OR

1. Create an ngrok account & authenticiate it on this machine with the auth token given on your profile page
2. Run this file in python, leave it running (you can edit it as it runs)
3. In a different terminal, type `ngrok http 5000`, leave it to run
4. Go to your Bot's Slack API 'Events Subscription' page (must be Bot owner or collaborator)
5. Take the Forwarding url for the ngrok terminal (ends with '-free.app') & copy it into the 'Request URL' bar, add '/slack/events' to the end, get it Verified 
6. SAVE THE CHANGES ON THAT PAGE
7. It should be working now–send it prompts through an Slack channel that Bot is
    connected through
#### Not Working?
- Double check you've connected the right Bot (right Bot's Slack API page, 
    token & signing secret)
- Make sure you've authenticated ngrok on local machine before running it
- Make sure url in ngrok terminal matches that in the 'Events Subscription' page
    - Make sure those CHANGES WERE SAVED THERE IS A 'SAVE CHANGES' BUTTON YOU MUST PRESS
- Make your sending the Bot's prompts in a channel where it's added
- Double check with channel id you're sending the Bot's responses to
