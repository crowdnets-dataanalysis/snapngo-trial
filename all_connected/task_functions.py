"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: All functions for the Task Generation Component.
"""
import random
import helper_functions

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
    db = helper_functions.connectDB('snapngo_db');

    # Get matrix representation of graph and dictionary of vertex indices & locations
    matrix, vertices = helper_functions.read_file("graph.txt")
    locations_list = list(vertices.values())

    # Generate a list of `num_tasks` task objects
    all_tasks = [create_task(locations_list) for _ in range(num_tasks)]

    # Insert those tasks objects into the Task database
    insert_tasks(all_tasks, db)

    # Close database connection
    db.close()


if __name__ == '__main__':
    # Testing create_task
    # Get matrix representation of graph and dictionary of vertex indices & locations
    matrix, vertices = helper_functions.read_file("graph.txt")
    locations_list = list(vertices.values())

    new_task = create_task(locations_list)
    print(new_task)