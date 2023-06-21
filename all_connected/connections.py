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

import time


### ### Control Center ### ###
DB_NAME = 'snapngo_test'

TASK_CYCLE = 2
NUM_TASKS_PER_CYCLE = 3

MATCHING_CYCLE = 3

MESSENGER_BOT_CYCLE = 5



### ### Task Generation call ### ###
# Generate & insert task(s)
def task_call():
    """Takes & returns nothing. Container for task call timer."""
    task.generate_tasks(NUM_TASKS_PER_CYCLE, DB_NAME)
    print('- tasks generated')

task_timer = helper_functions.RepeatTimer(task_call, TASK_CYCLE)


### ### Matching Algorithm & Assignments call ### ###
# Update expired tasks, matches unexpired & unassigned tasks to users, create those Assignments
def match_call():
    """Takes & returns nothing. Container for match call timer."""
    matching_assignments.match_users_and_tasks(matching_assignments.algorithm_random, DB_NAME)
    print("- tasks matched")


match_timer = helper_functions.RepeatTimer(match_call,
                                seconds=MATCHING_CYCLE,
                                minutes=0,
                                hours=0)


### ### MESSENGER call ### ###
# Sends out tasks & updates recommendTime in 'assignments' table
def messenger_bot_call():
    """Takes & returns nothing. Container for messenger timer."""
    assign_dict = messenger.get_assignments(DB_NAME)
    bot.send_tasks(assign_dict)
    print('- sent tasks')
    messenger.update_assign_status("pending", 0, 0)


messenger_timer = helper_functions.RepeatTimer(messenger_bot_call,
                                seconds=MESSENGER_BOT_CYCLE,
                                minutes=0,
                                hours=0)


if __name__ == "__main__":
    # Start all cycles
    task_timer.start()
    match_timer.start()
    messenger_timer.start()

    # Run time
    time.sleep(6)

    # End all cycles
    task_timer.cancel()
    match_timer.cancel()
    messenger_timer.cancel()
