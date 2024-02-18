"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: File that connects all 5 components & calls functions for them to 
    run the backend of Snap N Go.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

import matching_assignments
import task
import messenger
import bot
import task_parameters

from datetime import datetime as dt, date
import time
import schedule
from threading import Timer

### ### Control Center ### ###
DB_NAME = os.environ['DB_NAME']

TASK_CYCLE = task_parameters.TASK_CYCLE #every half an hour
NUM_TASKS_PER_CYCLE = task_parameters.NUM_TASKS_PER_CYCLE 

MATCHING_CYCLE = task_parameters.MATCHING_CYCLE

MESSENGER_BOT_CYCLE = task_parameters.MESSENGER_BOT_CYCLE 

START_HOURS = task_parameters.START_HOURS
END_HOURS = task_parameters.END_HOURS

# Researchers who are not regular participants 
admin_list = task_parameters.admin_list



class RepeatTimer(Timer):
    def __init__(self, func, seconds=10, minutes=0, hours=0):
        super().__init__(seconds + minutes*60 + hours*3600, func)
        func()

    def run(self):
        now = dt.now()
        not_weekend = now.strftime("%A").lower() not in {'saturday', 'sunday'}
        during_workday = START_HOURS < now.time() < END_HOURS
        while not self.finished.wait(self.interval):
            if not_weekend and during_workday:
                self.function(*self.args, **self.kwargs)


### ### Task Generation call ### ###
# Generate & insert task(s)
def task_call():
    """Takes & returns nothing. Container for task call timer."""
    task.generate_tasks(NUM_TASKS_PER_CYCLE, DB_NAME)
    print('- tasks generated', dt.now())


### ### Matching Algorithm & Assignments call ### ###
# Update expired tasks, matches unexpired & unassigned tasks to users, create those Assignments
def match_call():
    """Takes & returns nothing. Container for match call timer."""
    matching_assignments.match_users_and_tasks(task_parameters.MATCHING_ALGO, DB_NAME)
    print("- tasks matched", dt.now())


### ### MESSENGER call ### ###
# Sends out tasks & updates recommendTime in 'assignments' table
def messenger_bot_call():
    """Takes & returns nothing. Container for messenger timer."""
    assign_dict = messenger.get_assignments(DB_NAME)
    bot.send_tasks(assign_dict)
    print('- sent tasks')
    messenger.update_assign_status("pending", 0, 0)



def start_all_timers():
    task_timer = RepeatTimer(task_call, TASK_CYCLE)
    match_timer = RepeatTimer(match_call,
                                seconds=MATCHING_CYCLE,
                                minutes=0,
                                hours=0)
    messenger_timer = RepeatTimer(messenger_bot_call,
                                seconds=MESSENGER_BOT_CYCLE,
                                minutes=0,
                                hours=0)
    # Start all cycles
    task_timer.start()
    match_timer.start()
    messenger_timer.start()
    print("STARTED ALL TIMERS", dt.now())
    return task_timer, match_timer, messenger_timer

def cancel_all_timers(task_timer, match_timer, messenger_timer):
    print("CANCEL ALL TIMERS", dt.now())
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
    end_time = dt.combine(date.today(), END_HOURS)
    duration = (end_time - dt.now()).total_seconds()
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
    end_time = dt.combine(date.today(), END_HOURS)
    duration = (end_time - dt.now()).total_seconds()
    print(duration)
    time.sleep(duration + 2) # run till end_time
    # Check assignments and end daily summary
    bot.check_all_assignments()
    # End all cycles
    cancel_all_timers(task_timer, match_timer, messenger_timer)

if __name__ == "__main__":
    start_hours_str = START_HOURS.strftime("%H:%M")

    schedule.every().monday.at(start_hours_str).do(short_cycle)
    schedule.every().tuesday.at(start_hours_str).do(short_cycle)
    schedule.every().wednesday.at(start_hours_str).do(short_cycle)
    schedule.every().thursday.at(start_hours_str).do(short_cycle)
    schedule.every().friday.at(start_hours_str).do(short_cycle)
    schedule.every().saturday.at(start_hours_str).do(short_cycle)
    schedule.every().sunday.at(start_hours_str).do(short_cycle)
    
    while True:
        schedule.run_pending()
        time.sleep(1)