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
    if table_name == 'users':
        cursor.execute(f"SELECT * FROM {table_name} WHERE `status` = 'active';")
    else:
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

def create_ab_groups(user_list):
    middle_index = int(len(user_list)/2)
    a_group = user_list[:middle_index]
    b_group = user_list[middle_index:]
    return a_group, b_group

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

def algorithm_weighted(assignment_data, task_data, user_data):
    """
    * One of many possible matching algorithms for match_users_and_tasks()*
    Takes a list of all user ids & a list of all unassigned task ids.
    Matches a user (who has never been previously assigned to this task) to each task weighted on their reliability scores.
    Returns a list of those user-task matches, format: [[task_id, user_id], [...], ...]
    """
    # Assemble task-user dict, key: task_id (int), value: ids of all previously-assigned users (set)
    task_users_dict = {} if not assignment_data else create_task_user_dict(assignment_data)
    reliability_dict = {user_data['id'][i]:float(user_data['reliability'][i]) for i in range(len(user_data['id']))}
    
    # Split users into ab groups
    # active_list = [user for user in reliability_dict if reliability_dict[user]> 0.1]
    # a_active, b_active = create_ab_groups(active_list)
    # inactive_list = [user for user in reliability_dict if reliability_dict[user]== 0.1]
    # a_inactive, b_inactive = create_ab_groups(inactive_list)
    # a_group = a_active + a_inactive
    # b_group = b_active + b_inactive
    # print("A GROUP: ", a_group)
    # print("B GROUP: ", b_group)
    a_group = ['U05EX6F89BR', 'U05F44JN6HL', 'U05FAPY69PU', 'U05FCBGTX1R', 'U05B24S3LR1', 'U05E80KQ9D0', 'U05EW82D1E3', 'U05EW84936K', 'U05F44J029L', 'U05F7RYS093', 'U05FALCSWJF']
    b_group = ['U05FMEAE62E', 'U05FPRMEMRS', 'U05G0FC05MW', 'U05G1M69C1E', 'U05FC4JJNUS', 'U05FCMQN908', 'U05FD7ERYMS', 'U05FE5S1BEG', 'U05FPD1KKLZ', 'U05G0FB3QKA', 'U05G0FC35CY']
    # For each task, select a new random user_id 
    matchings = []
    count = 0
    half_task = int(len(task_data)/2)
    for task_id in task_data:
        if count <= half_task:
            # Subtract all previously-assigned users from overall user pool
            available_user_ids = set(b_group) - task_users_dict.get(task_id, set())
            reliability_list = [int(reliability_dict[user]*100) for user in available_user_ids]

            # Assign & note matching
            user_id = random.choices(list(available_user_ids), reliability_list)[0]
        else:
            available_user_ids = set(a_group) - task_users_dict.get(task_id, set())

            # Assign & note matching
            user_id = random.choice(list(available_user_ids))
        matchings.append([task_id, user_id])
        count += 1
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
    # task_data = read_table(db, 'tasks')
    user_data = read_table(db, 'users')

    # Updates task expiration status
    cursor = db.cursor()
    cursor.execute(f"UPDATE tasks SET expired = 1 WHERE start_time + INTERVAL time_window minute < now()")
    
    # Identify unassigned tasks 
    cursor.execute(f"SELECT tasks.id FROM tasks LEFT JOIN assignments ON tasks.id=assignments.task_id \
                   WHERE expired = 0 AND tasks.id NOT IN (SELECT task_id from assignments)")
    unassigned_tasks = set([tasks[0] for tasks in cursor.fetchall()])
    # Use the given Matching Algorithm to match users to unassigned tasks
    if user_data:
        task_user_matchings = matching_algo(assignment_data, unassigned_tasks, user_data)

        # Generate Assignments & insert them into the Assignments table
        all_assignments = [{'task_id': task_id, 'user_id': user_id} for task_id, user_id in task_user_matchings]
        insert_assignments(all_assignments, db)

    # Close database connection
    db.close()



if __name__ == '__main__':
    match_users_and_tasks(algorithm_weighted, 'snapngo_db')
