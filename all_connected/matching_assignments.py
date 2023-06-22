"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: All functions & algorithms for the Matching Component & Assignment generation.
"""

import random
import pymysql
import helper_functions
from datetime import datetime

### ### SPECIFIC HELPER FUNCTIONS ### ###
def read_table(db, table_name):
    """
    * Helper function for match_users_and_tasks()*
    Takes (str) database name and (str) table name.
    Reads data from that table.
    Returns data as a dict w/ column names (keys) and list of column values (values)
    """
    # Create Dict cursor object & fetch all data in the table
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM {table_name};")
    table_data = cursor.fetchall()
    
    # Returns {} if table is empty
    if not table_data: 
        return table_data 

    # Reorder data into: col_name (keys), list of values (values)
    table_dict = {k:[] for k in table_data[0].keys()}
    for row in table_data:
        for col_name in row:
            table_dict[col_name].append(row[col_name])

    return table_dict


def create_task_user_dict(assignment_data):
    """
    * Helper functions for matching algorithms * 
    Takes data from the 'assignments' table (dict).
    Creates a task-user dict, key: task_id, value: set of all user_ids who've 
        previously been assigned to it.
    Returns that dict.
    """
    # get [task_id, user_id] pairs
    task_user_list = list(zip(assignment_data['task_id'], assignment_data['user_id']))
    
    # map all user_ids (values) to task_id (key) 
    task_users_dict = {}
    for task_id, user_id in task_user_list:
        previously_assigned = task_users_dict.get(task_id, set()) # get any user_ids already stored
        previously_assigned.add(user_id)
        task_users_dict[task_id] = previously_assigned

    return task_users_dict


def insert_assignments(assignment_info, db):
    """
     * Helper function for match_users_and_tasks() *
    Takes a list of assignments and database (obj).
    Inserts the assignments into the database given. 
    Returns nothing.
    """
    # Connect to database & create cursor obj
    cursor = db.cursor()

    for assignment in assignment_info:
        # Create & execute query
        query = f"INSERT INTO assignments(`task_id`, `user_id`, `status`) VALUES \
            ({assignment['task_id']}, '{assignment['user_id']}', 'not assigned');"
        cursor.execute(query)

        # Commit the changes to the database
        db.commit()



### ### ALGORITHMS ### ###
def algorithm_random(assignment_data, task_data, user_data):
    """
    * One of many possible matching algorithms for match_users_and_tasks()*
    Takes a list of all user ids & a list of all unassigned task ids.
    Randomly matches a user (who has never been previously assigned to this task) to each task.
    Returns a list of those user-task matches, format: [[task_id, user_id], [...], ...]
    """
    # Assemble task-user dict, key: task_id (int), value: ids of all previously-assigned users (set)
    task_users_dict = {} if not assignment_data else create_task_user_dict(assignment_data)

    # For each task, select a new random user_id 
    matchings = []
    for task_id in task_data:
        # Subtract all previously-assigned users from overall user pool
        available_user_ids = set(user_data['id']) - task_users_dict.get(task_id, set())

        # Assign & note matching
        user_id = random.choice(list(available_user_ids))
        matchings.append([task_id, user_id])

    return matchings



### ### OVERALL MATCHING & ASSIGNMENT GENERATION ### ###
def match_users_and_tasks(matching_algo, db_name):
    """
    Takes 'users' table data & 'tasks' table data, and a matching algorithm (function).
    Finds unexpired & unassigned tasks, matches users to those tasks, writes those
        Assignments to the 'assignments' table.
    Returns nothing.
    """
    # Open database connection
    db = helper_functions.connectDB(db_name)

    # read in assignment, task, and user data
    assignment_data = read_table(db, 'assignments')
    task_data = read_table(db, 'tasks')
    user_data = read_table(db, 'users')

    # Updates task expiration status
    cursor = db.cursor()
    cursor.execute(f"UPDATE tasks SET expired = 1 WHERE start_time + INTERVAL time_window minute < now()")
    
    # Identify unassigned tasks 
    cursor.execute(f"SELECT tasks.id FROM tasks LEFT JOIN assignments ON tasks.id=assignments.task_id \
                   WHERE expired = 0 AND tasks.id NOT IN (SELECT task_id from assignments)")
    unassigned_tasks = set([tasks[0] for tasks in cursor.fetchall()])

    # Use the given Matching Algorithm to match users to unassigned tasks
    task_user_matchings = matching_algo(assignment_data, unassigned_tasks, user_data)

    # Generate Assignments & insert them into the Assignments table
    all_assignments = [{'task_id': task_id, 'user_id': user_id} for task_id, user_id in task_user_matchings]
    insert_assignments(all_assignments, db)

    # Close database connection
    db.close()



if __name__ == '__main__':
    match_users_and_tasks(algorithm_random, 'snapngo_test')
