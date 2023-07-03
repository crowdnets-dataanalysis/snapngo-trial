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

import time


import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

import messenger

import json
import requests
import copy
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler

from datetime import datetime, timedelta, time, date
import schedule


### ### Control Center ### ###
DB_NAME = 'snapngo_db'

START_HOURS = helper_functions.START_HOURS
END_HOURS = helper_functions.END_HOURS


def add_new_users():
    user_store = bot.get_all_users_info()
    messenger.add_users(user_store)

def delete_invalid_submissions(user_id, task_id, assignment_id):

    message = []
    bot.send_messages(user_id, message, "invalid submission")
    return


if __name__ == "__main__":
    #users_store = bot.get_all_users_info()
    #bot.send_welcome_message({'U05B24S3LR1': ['helen'], 'U05FCMQN908':['cj']})
    #messenger.delete_submission(user_id, task_id)
    #bot.check_all_assignments()
    user_store = bot.get_all_users_info()
    messenger.add_users(user_store)
    bot.send_welcome_message(user_store)
