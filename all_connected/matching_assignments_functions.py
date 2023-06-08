"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: All functions & algorithms for the Matching Component & Assignment generation.
"""

import random
import helper_functions

### ### USER-TASK MATCHING ### ###
def read_table(db, table_name):
    """
    * Helper function for match_users_and_tasks()*
    Takes (str) database name and (str) table name.
    Reads data from that table.
    Returns data as a dict w/ column names (keys) and list of column values (values)
    """
    # Create cursor object
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table_name};")
    table_data = cur.fetchall()[0]

    # format data -> dict w/ column names (keys) and list of column values (values) 
    raise NotImplementedError

    return table_data


def find_unassigned_tasks(task_data):
    """
    Takes 'tasks' table data.
    Identifies unassigned tasks,
    Returns a list of task ids that aren't assigned
    """
    # discuss w/ chrsitine about how we should identify unassigned tasks
    # by expired? How should we write expired? Start time starts at recced time?
    raise NotImplementedError 


def create_task_user_dict(assignment_data):
    """
    * Helper functions for matching algorithms * 
    Takes data from the 'assignments' table (dict).
    Creates a task-user dict, key: task_id, value: set of all user_ids who've been assigned to it
    Returns that dict.
    """
    # get [task_id, user_id] pairs
    task_user_list = list(zip(assignment_data['taskID'], assignment_data['userID']))
    
    # map all user_ids (values) to task_id (key) 
    task_users_dict = {}
    for task_id, user_id in task_user_list:
        previously_assigned = task_users_dict.get(task_id, set()) # get any user_ids already stored
        previously_assigned.add(user_id)
        task_users_dict[task_id] = previously_assigned

    return task_users_dict


def algorithm_random(assignment_data, task_data, user_data):
    """
    * One of many possible matching algorithms for match_users_and_tasks()*
    Takes a list of all user ids & a list of all unassigned task ids
    Randomly matches a user to each task.
    Returns a list of those user-task matches, format: [[task_id, user_id], [...], ...]
    """
    # Assemble task-user dict, key: task_id (int), value: ids of all previously-assigned users (set)
    task_users_dict = create_task_user_dict(assignment_data)

    # For each task, select a new random user_id 
    matchings = []
    for task_id in task_data['id']:
        # Subtract all previously-assigned users from overall user pool
        available_user_ids = set(user_data['id']) - task_users_dict.get(task_id, set())

        # Assign & note matching
        user_id = random.choice(available_user_ids)
        matchings.append([task_id, user_id])

    return matchings


def match_users_and_tasks(matching_algo, db_name):
    """
    Takes 'users' table data & 'tasks' table data, and a matching algorithm (function)
    Match a user to each task using the given algorithm, 
    """
    # Open database connection
    db = helper_functions.connectDB(db_name)

    # read in assignment, task, and user data
    assignment_data = read_table(db, 'assignments')
    task_data = read_table(db, 'tasks')
    user_data = read_table(db, 'users')

    # identify unassigned tasks 
    unassigned_tasks = find_unassigned_tasks(task_data)

    # Use the given Matching Algorithm to match users to unassigned tasks
    task_user_matchings = matching_algo(unassigned_tasks, assignment_data, task_data, user_data)

    # Generate a list assignment objects from task-user matchings
    all_assignments = [create_assignment(info) for info in task_user_matchings]

    # Insert those assignment objects into the Assignment database
    insert_assignments(all_assignments, db)

    # Close database connection
    db.close()



### ### ASSIGNMENT GENERATION ### ###
def create_assignment(assignment_info):
    """
     * Helper function for generate_assignments() *
     * this function exists to clarify the assignment generation process *
    Takes (list) assignment info (task_id (int) and user_id (int)), likely from the Matching 
        Algorithm.
    Returns a dict of relevant values (all others will be determined and written in later).
    
    """
    task_id, user_id = assignment_info
    return {'task_id': task_id, 
            'user_id': user_id}


def insert_assignments(assignments_list, db):
    """
     * Helper function for generate_assignments() *
    Takes a list of assignments and database (obj).
    Inserts the assignments into the database given. 
    Returns nothing.
    """
    # Connect to database & create cursor obj
    cursor = db.cursor()

    for assignment in assignments_list:
        # Create & execute query
        query = f"INSERT INTO Assignments(task_id, user_id) VALUES ({assignment['task_id']}, \
            {assignment['user_id']})"
        cursor.execute(query)

        # Commit the changes to the database
        db.commit()


def generate_assignments(assignment_info_list):
    """
    Takes a list of assignment info (from the Matching Algorithm).
    Creates those assignments & inserts them into the Assignments database.
    Returns nothing.
    """
    # Open database connection
    db = helper_functions.connectDB('snapngo_db');

    # Generate a list assignment objects from assignment data
    all_assignments = [create_assignment(info) for info in assignment_info_list]

    # Insert those assignment objects into the Assignment database
    insert_assignments(all_assignments, db)

    # Close database connection
    db.close()




if __name__ == '__main__':
    # ASSIGNMENTS
    assign_info = [1, 3] # task id, user id
    new_assignment = create_assignment(assign_info)
    print(new_assignment)

    t1 = [1,2,3,4,4,3] # task_id
    t2 = [5,6,7,8,5,9]
    task_user_list = list(zip(t1, t2))
    task_users = {}
    for task_id, user_id in task_user_list:
        assign = task_users.get(task_id, set())
        assign.add(user_id)
        task_users[task_id] = assign

    print(res2)
