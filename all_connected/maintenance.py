"""
Name: Helen Mao
Date: 06/26/2023
Description: Maintenance file for Snap N Go. Can be used to apply immediate
        fix while the bot and connections file are running.
"""
import helper_functions
import matching_assignments
import task
import messenger
import bot
import task_parameters

import time


import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

import json
import requests
import copy
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler

from datetime import datetime, timedelta, time, date
#import schedule


### ### Control Center ### ###
DB_NAME = os.environ['DB_NAME']

START_HOURS = task_parameters.START_HOURS
END_HOURS = task_parameters.END_HOURS

def add_new_users():
    user_store = bot.get_all_users_info()
    messenger.add_users(user_store)

def delete_invalid_submissions(user_id, task_id, assignment_id):
    message = []
    bot.send_messages(user_id, message, "invalid submission")
    return

def broadcast(block = None, text = None):
    active_users = messenger.get_active_users_list()
    for user_id in active_users:
        bot.send_messages(user_id, block = None, text = None)

def test_update_reliability(user_id):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    date = datetime.today().strftime('%Y/%m/%d')
    print(date)
    query = f'''SELECT task_id
                FROM assignments
                WHERE (user_id = '{user_id}') and DATE(recommend_time) >= CURDATE() -1
            '''
    cur.execute(query)
    accepted = cur.fetchall()
    print(accepted)

if __name__ == "__main__":
    add_new_users()
    print("DONE")