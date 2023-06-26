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


### ### Control Center ### ###
DB_NAME = 'snapngo_db'

def add_new_users():
    user_store = bot.get_all_users_info()
    messenger.add_users(user_store)


if __name__ == "__main__":
    add_new_users()
