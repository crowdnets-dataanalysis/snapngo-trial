"""
Author: Sofia Kobayashi
Date: 06/06/2023
Description: Tests & reference on how to send a message from the backend -> Slack user
    via a Slack Bot. This message is prompted by running this file.
    Also a test & reference for connecting to our local SQL database.

Steps to connect to the SQL database through the terminal.
1. Get into directory where the .bash_file with the path to your SQL db is
2. Run `source .bash_profile` (should return nothing)
3. Run `mysql -u root -p`
* SQL password for Sofia's computer: '12345678'
* SQL password for the CrowdNets computer (as of 06/09/23): 'EHcr0wdNet$KS'
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from slack_sdk import WebClient
import pymysql


# Set up environment (to get passwords/tokens from your .env file)
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

# Connect to local SQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password=os.environ['SQL_PASS'],
    db='snapngo_test'
)

# Get data from 
cur = conn.cursor()
cur.execute("USE snapngo_test;")
cur.execute("SELECT * from users WHERE id = 0;")
output = cur.fetchall()[0]
conn.close()

# Create client obj to connect to Slack Bot
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Send the specified message to specified channel BY RUNNING THIS PYTHON FILE
client.chat_postMessage(channel='#bot-testing', 
                        text=f'(From SQL database) User #{output[0]}: {output[1]}, with ${output[2]}!')