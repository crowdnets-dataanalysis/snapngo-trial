"""
Name: Sofia Kobayashi, based on work from Amy Fung & Cynthia Wang
Date: 06/07/2023
Description: All functions for the Task Generation Component.
"""
import random
import json
import helper_functions
from datetime import datetime, timedelta, time, date
import pandas as pd 


START_HOURS = time(10,00) # 10am
END_HOURS = time(16,00) # 4pm

### ### HELPER FUNCTIONS ### ###
def random_datetime(n):
    """
    * Helper function for create_task() *
    Takes number of random dates to generate.
    Generates a random datetime with the limit specified below.
    Returns a random datetime.
    """    
    # Get start times
    now = datetime.strptime('2023-06-22 20:35:30', '%Y-%m-%d %H:%M:%S')
    
    # If today's a weekend or after hours on friday -> start = next monday at start_hours
    weekday = now.strftime("%A").lower()
    if weekday in {'saturday', 'sunday'} or (weekday == 'friday' and now.time() > END_HOURS):
        date = datetime.now() + timedelta(days=-now.date().weekday(), weeks=1) # next monday
        start = datetime.combine(date, START_HOURS)   
    # If weekday, but before 10am -> start = today at start_hours
    elif now.time() < START_HOURS:
        start = datetime.combine(date.date(), START_HOURS)
    # If weekday, during hours -> start time = now
    elif START_HOURS < now.time() < END_HOURS:
        start = now
    # If weekday (except friday), after hours -> start time = next day at start_hours
    else:
        start = datetime.combine((now + timedelta(hours=24)), START_HOURS)
    
    # Get end time
    end = datetime.combine(start.date(), END_HOURS) + timedelta(hours=1)

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
        query = f"INSERT INTO Tasks(location, time_window, compensation, expired, description, start_time) \
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
    res = random_datetime(7)
    print(res)