"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: File that connects all 5 components & calls functions for them to 
    run the backend of Snap N Go.
"""
import helper_functions
import matching_assignments
import task

### ### Control Center ### ###
DB_NAME = 'snapngo_test'

TASK_CYCLE = 5
NUM_TASKS_PER_CYCLE = 3

MATCHING_CYCLE = 6

MESSENGER_CYCLE = 15



### ### Task Generation call ### ###
# Generate & insert task(s)
task.generate_tasks(NUM_TASKS_PER_CYCLE, DB_NAME)


### ### Matching Algorithm & Assignments call ### ###
# Update expired tasks, matches unexpired & unassigned tasks to users, create those Assignments
matching_assignments.match_users_and_tasks(matching_assignments.algorithm_random, DB_NAME)


### ### MESSENGER call ### ###


pass