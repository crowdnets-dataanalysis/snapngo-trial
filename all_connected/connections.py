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

TASK_CYCLE = 5
NUM_TASKS_PER_CYCLE = 3

MATCHING_CYCLE = 6

MESSENGER_CYCLE = 15



### ### Task Generation call ### ###
# Generate & insert task(s)
def task_call():
    """Takes & returns nothing. Container for task call timer."""
    task.generate_tasks(NUM_TASKS_PER_CYCLE, DB_NAME)

task_timer = helper_functions.RepeatTimer(task_call,2)


### ### Matching Algorithm & Assignments call ### ###
# Update expired tasks, matches unexpired & unassigned tasks to users, create those Assignments
def match_call():
    """Takes & returns nothing. Container for match call timer."""
    matching_assignments.match_users_and_tasks(matching_assignments.algorithm_random, DB_NAME)
    print("tasks matched")


match_timer = helper_functions.RepeatTimer(match_call,
                                seconds=10,
                                minutes=0,
                                hours=0)


### ### MESSENGER call ### ###
# Sends out tasks & uodates recommendTime in 'assignments' table
unassigned_info = [0]
# print("unassigned_info: '', ", unassigned_info)
def messenger_call():
    """Takes & returns nothing. Container for messenger timer."""
    unassigned_info[0] = messenger.getAssignments(DB_NAME)
    print("get unassigned tasks: ", unassigned_info)


messenger_timer = helper_functions.RepeatTimer(messenger_call,
                                seconds=10,
                                minutes=0,
                                hours=0)


### ### BOT call ### ###
# Sends tasks to users over Slack
def bot_call():
    """Takes & returns nothing. Container for bot timer."""
    print("unassigned_info: ", unassigned_info[0])
    bot.sendTasks(unassigned_info[0])

bot_timer = helper_functions.RepeatTimer(bot_call,
                                seconds=10,
                                minutes=0,
                                hours=0)



task_timer.start()
match_timer.start()
messenger_timer.start()
bot_timer.start()

time.sleep(2)
task_timer.cancel()
match_timer.cancel()
messenger_timer.cancel()
bot_timer.cancel()