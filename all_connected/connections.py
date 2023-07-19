"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: File that connects all 5 components & calls functions for them to 
    run the backend of Snap N Go.
"""
import helper_functions
import matching_assignments
import task
import messenger
import bot

import datetime
import time
import schedule

### ### Control Center ### ###
DB_NAME = 'snapngo_db'

TASK_CYCLE = 30*60
NUM_TASKS_PER_CYCLE = messenger.get_total_users()*2

MATCHING_CYCLE = TASK_CYCLE+2

MESSENGER_BOT_CYCLE = 60*60+3


START_HOURS = helper_functions.START_HOURS
END_HOURS = helper_functions.END_HOURS

admin_list = ["U05BL0N0G2V", "U05B24S3LR1", "U051SER8FNU", "U05BRV5FE7J", "U05DBM3U3DM"]

### ### Task Generation call ### ###
# Generate & insert task(s)
def task_call():
    """Takes & returns nothing. Container for task call timer."""
    task.generate_tasks(NUM_TASKS_PER_CYCLE, DB_NAME)
    print('- tasks generated', datetime.datetime.now())


### ### Matching Algorithm & Assignments call ### ###
# Update expired tasks, matches unexpired & unassigned tasks to users, create those Assignments
def match_call():
    """Takes & returns nothing. Container for match call timer."""
    matching_assignments.match_users_and_tasks(matching_assignments.algorithm_weighted, DB_NAME)
    print("- tasks matched", datetime.datetime.now())


### ### MESSENGER call ### ###
# Sends out tasks & updates recommendTime in 'assignments' table
def messenger_bot_call():
    """Takes & returns nothing. Container for messenger timer."""
    assign_dict = messenger.get_assignments(DB_NAME)
    bot.send_tasks(assign_dict)
    print('- sent tasks')
    messenger.update_assign_status("pending", 0, 0)



def start_all_timers():
    task_timer = helper_functions.RepeatTimer(task_call, TASK_CYCLE)
    match_timer = helper_functions.RepeatTimer(match_call,
                                seconds=MATCHING_CYCLE,
                                minutes=0,
                                hours=0)
    messenger_timer = helper_functions.RepeatTimer(messenger_bot_call,
                                seconds=MESSENGER_BOT_CYCLE,
                                minutes=0,
                                hours=0)
    # Start all cycles
    task_timer.start()
    match_timer.start()
    messenger_timer.start()
    print("STARTED ALL TIMERS", datetime.datetime.now())
    return task_timer, match_timer, messenger_timer

def cancel_all_timers(task_timer, match_timer, messenger_timer):
    print("CANCEL ALL TIMERS", datetime.datetime.now())
    task_timer.cancel()
    match_timer.cancel()
    messenger_timer.cancel()

def daily_cycle():
    all_users = messenger.get_all_users_list()
    for user_id in all_users:
        if user_id not in admin_list:
            messenger.update_account_status(user_id, "active")
    task_timer, match_timer, messenger_timer = start_all_timers()
    # Run time
    end_time = datetime.datetime.combine(datetime.date.today(), END_HOURS)
    duration = (end_time - datetime.datetime.now()).total_seconds()
    print(duration)
    time.sleep(duration + 2) # run till end_time
    # Check assignments and end daily summary
    bot.check_all_assignments()
    for user_id in all_users:
        if user_id not in ['USLACKBOT']:
            messenger.update_reliability(user_id)
    # End all cycles
    cancel_all_timers(task_timer, match_timer, messenger_timer)

def short_cycle():
    all_users = messenger.get_all_users_list()
    for user_id in all_users:
        if user_id not in admin_list:
            messenger.update_account_status(user_id, "active")
    task_timer, match_timer, messenger_timer = start_all_timers()
    # Run time
    end_time = datetime.datetime.combine(datetime.date.today(), END_HOURS)
    duration = (end_time - datetime.datetime.now()).total_seconds()
    print(duration)
    time.sleep(duration + 2) # run till end_time
    # Check assignments and end daily summary
    bot.check_all_assignments()
    # End all cycles
    cancel_all_timers(task_timer, match_timer, messenger_timer)

if __name__ == "__main__":
    # user_store = bot.get_all_users_info()
    # messenger.add_users(user_store)
    # #bot.send_welcome_message(user_store)

    # Start all cycles
    # start_all_timers()

    # # Run time
    # time.sleep(3*60*60*24) # run for three days

    # # End all cycles
    # task_timer.cancel()
    # match_timer.cancel()
    # messenger_timer.cancel()

    # Try implementing using schedule library
    #schedule.every().day.at("16:40").do(cancel_all_timers)
    # daily_cycle()
    schedule.every().day.at("10:07").do(daily_cycle)
    
    while True:
        schedule.run_pending()
        time.sleep(1)