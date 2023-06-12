"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: File that connects all 5 components & calls functions for them to 
    run the backend of Snap N Go. TEST
"""
import helper_functions
import matching_assignments
import task
# import messenger
# import bot

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

task_timer = helper_functions.RepeatTimer(task_call,
                                seconds=10,
                                minutes=0,
                                hours=0)



### ### Matching Algorithm & Assignments call ### ###
# Update expired tasks, matches unexpired & unassigned tasks to users, create those Assignments
def match_call():
    """Takes & returns nothing. Container for match call timer."""
    matching_assignments.match_users_and_tasks(matching_assignments.algorithm_random, DB_NAME)

match_timer = helper_functions.RepeatTimer(match_call,
                                seconds=10,
                                minutes=0,
                                hours=0)


### ### MESSENGER call ### ###
# Sends out tasks & uodates recommendTime in 'assignments' table
unassigned_info = [0]
def messenger_call():
    """Takes & returns nothing. Container for match messenger timer."""
    unassigned_info = matching_assignments.match_users_and_tasks(matching_assignments.algorithm_random, DB_NAME)

messenger_timer = helper_functions.RepeatTimer(messenger_call,
                                seconds=10,
                                minutes=0,
                                hours=0)

unassigned_info = messenger.get_unassgined_assignments(DB_NAME)


### ### BOT call ### ###
# Sends tasks to users over Slack
# bot.send_tasks(unassigned_info)
