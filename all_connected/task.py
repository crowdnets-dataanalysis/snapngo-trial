"""
Name: Sofia Kobayashi, based on work from Amy Fung & Cynthia Wang
Date: 06/07/2023
Description: All functions for the Task Generation Component.
"""
import random
import json
import helper_functions
from datetime import datetime, timedelta
import pandas as pd 

### ### HELPER FUNCTIONS ### ###
def random_datetime(n):
    """
    * Helper function for create_task() *
    Takes number of random dates to generate.
    Generates a random datetime with the limit specified below.
    Returns a random datetime.
    """
    # Define start/end times
    start = datetime.now()
    end = datetime.now() + timedelta(hours=5)
    
    # Generate & choose n random dates
    dates = pd.date_range(start, end, freq='1min').to_series()
    date_sample = [str(date)[:-7] for date in dates.sample(5, replace=True).to_list()]

    return date_sample


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
    
    with open('data/task_descriptions.json', 'r') as infile:
        all_descriptions = json.load(infile)

    return {'location': location,
            'time_window': random.randint(1, 100),
            'compensation': round(random.randint(40, 60)/100, 2),
            'expired': False,
            'description': f'At {location} in the Science Center, {random.choice(all_descriptions)}'}


def insert_tasks(db, tasks_list, start_times):
    """
     * Helper function for generate_tasks() *
    Takes a list of tasks and database (obj).
    Inserts the tasks into the database given. 
    Returns nothing.
    """
    # Connect to database & a cursor object
    cursor = db.cursor()

    for i, task in enumerate(tasks_list):
        # Create & execute query
        query = f"INSERT INTO Tasks(location, time_window, compensation, expired, description, starttime) \
            VALUES('{task['location']}', {task['time_window']}, {task['compensation']}, \
                {task['expired']}, '{task['description']}', '{start_times[i]}')"
        cursor.execute(query)

        # Commit the changes to the database
        db.commit()




### ### OVERALL TASK GENERATION ### ###
def generate_tasks(num_tasks, db_name):
    """
    Takes number of tasks to be generated.
    Creates those tasks & inserts them into the Tasks database.
    Returns nothing.
    """
    # Open database connection
    db = helper_functions.connectDB(db_name);

    # Get matrix representation of graph and dictionary of vertex indices & locations
    with open('data/task_locations.json', 'r') as infile:
        locations_list = json.load(infile)

    # Generate a Tasks & random start times
    all_tasks = [create_task(locations_list) for _ in range(num_tasks)]
    start_times = random_datetime(num_tasks)

    # Insert those tasks objects into the Task database
    insert_tasks(db, all_tasks, start_times)

    # Close database connection
    db.close()


if __name__ == '__main__':
    generate_tasks(3, 'snapngo_test')
