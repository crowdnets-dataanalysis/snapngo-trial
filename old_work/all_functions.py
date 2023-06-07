"""
Name: Sofia Kobayashi
Date: 06/07/2023
Reworking all pre-existing snap N go functions to work with current framework.
"""
import os
from pathlib import Path
import pymysql
from dotenv import load_dotenv
import random

from flask import Flask

import loadGraph


# setting up .env path (for keeping confidential data confidential)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def connectDB(dbName):
    """
     * General Helper Function * 
    Takes a database name (str).
    Returns a connection object to that database. This connection should eventually
        be closed with .close()
    """
    # Connect to the database
    db = pymysql.connect(
        host='localhost',
        user='root', 
        password=os.environ['SQL_PASS'], 
        db=dbName
    )

    return db




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
    db = connectDB('snapngo_db');

    # Generate a list assignment objects from assignment data
    all_assignments = [create_assignment(info) for info in assignment_info_list]

    # Insert those assignment objects into the Assignment database
    insert_assignments(all_assignments, db)

    # Close database connection
    db.close()


def insert_tasks(tasks_list, db):
    """
     * Helper function for generate_tasks() *
    Takes a list of tasks and database (obj).
    Inserts the tasks into the database given. 
    Returns nothing.
    """
    # Connect to database & a cursor object
    cursor = db.cursor()

    for task in tasks_list:
        # Create & execute query
        query = f"INSERT INTO Tasks(location, window, compensation, expired) VALUES \
            ({task['location']}, {task['window']}, {task['compensation']}, {task['expired']})"
        cursor.execute(query)

        # Commit the changes to the database
        db.commit()


def create_task(locations):
    """
     * Helper function for generate_tasks() *
    Takes a list of task locations.
    Generates a task object - random: location, window, compensation, expired set 
        to FALSE, all other features to be determined & added later.
    Returns a task object.
    """
    # Generate a random location, time window (seconds), and compensation (cents)
    location = random.choice(locations)
    window = random.randint(1, 100)
    compensation = random.randint(40, 60)

    # Return task object
    return {'location': location,
            'window': window,
            'compensation': compensation,
            'expired': False}

def generate_tasks(num_tasks):
    """
    Takes number of tasks to be generated.
    Creates those tasks & inserts them into the Tasks database.
    Returns nothing.
    """
    # Open database connection
    db = connectDB('snapngo_db');

    # Get matrix representation of graph and dictionary of vertex indices & locations
    matrix, vertices = loadGraph.read_file("graph.txt")
    locations_list = list(vertices.values())

    # Generate a list of `num_tasks` task objects
    all_tasks = [create_task(locations_list) for _ in range(num_tasks)]

    # Insert those tasks objects into the Task database
    insert_tasks(all_tasks, db)

    # Close database connection
    db.close()

if __name__ == '__main__':
    # ASSIGNMENTS
    assign_info = [1, 3] # task id, user id
    new_assignment = create_assignment(assign_info)
    print(new_assignment)

    # TASKS
    # Get matrix representation of graph and dictionary of vertex indices & locations
    matrix, vertices = loadGraph.read_file("graph.txt")
    locations_list = list(vertices.values())

    new_task = create_task(locations_list)
    print(new_task)