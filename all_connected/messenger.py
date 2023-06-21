"""
terminal command to get into SQL:
source .bash_profile
mysql -u root -p
to get slack running:
ngrok http 5000 (in one terminal)
run this file in another terminal
(both of these things need to happen in order to run)
"""
import helper_functions

### ### CONSTANTS ### ###
DB_NAME = "snapngo_test" 


def add_users(user_store):
    '''
    Gets teh database connection. Returns nothing.
    Add users to the database based on the current list of users in the the workplace 
    '''
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    # user_store = get_all_users_info()
    query1 = '''SELECT id FROM users'''
    cur.execute(query1)
    existing_ids = cur.fetchall()
    existing_ids = [id[0] for id in existing_ids]
    #print(existing_ids)
    query2 = '''INSERT INTO users (name, id) VALUES (%s, %s)'''
    for key in user_store:
        not_exist = key not in existing_ids
        not_bot = user_store[key]['is_bot'] == False
        not_slackbot = (key != 'USLACKBOT')
        if not_exist and not_bot and not_slackbot:
            name = user_store[key]['name']
            cur.execute(query2, (name, key))
            conn.commit()
    conn.close()

def update_tasks_expired():
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET `expired` = 1 WHERE (starttime + INTERVAL time_window MINUTE) < NOW()")
    conn.commit()
    conn.close

def get_task_list(user_id, task_id):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT assignments.taskID, assignments.userID, 
                tasks.location, tasks.description, tasks.starttime, tasks.time_window, 
                tasks.compensation
                FROM assignments INNER JOIN tasks ON assignments.taskID = tasks.id
                WHERE (assignments.taskID = {task_id} AND assignments.userID = '{user_id}')'''
    cur.execute(query)
    assignment = cur.fetchone()
    conn.close()
    assert assignment, F"Assignment #{task_id} could not be found in database!"
    return assignment


def get_assignments(db_name):
    '''
    Get all the assignments with status 'not assigned' together with each task's details. 
    Create a dictionary with keys being user ids and values being a list of tasks (with
    details) that user is assigned
    Return the dictionary
    '''
    update_tasks_expired()
    conn = helper_functions.connectDB(db_name)
    cur = conn.cursor()
    #print("finished1")
    query = '''SELECT assignments.taskID, assignments.userID, 
                tasks.location, tasks.description, tasks.starttime, tasks.time_window, 
                tasks.compensation
                FROM assignments INNER JOIN tasks ON assignments.taskID = tasks.id
                WHERE (assignments.status = 'not assigned' AND tasks.expired != 1)'''
    cur.execute(query)
    assignments = cur.fetchall()
    conn.close()
    #print(assignments)
    assignments_dict = {}
    for assignment in assignments:
        uid = assignment[1]
        #print(uid)
        if uid in assignments_dict:
            (assignments_dict[uid]).append(assignment)
        else:
            assignments_dict[uid] = [assignment]       
    #print(assignmentsDict)
    return assignments_dict

def get_assign_status(task, user):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT status FROM assignments
                WHERE taskID = {task} AND userID = '{user}'
    '''
    cur.execute(query)
    status = cur.fetchone()[0]
    return status


def update_assign_status(status, task_id, user_id):
    '''
    Takes database name, the new status of the assignment, the task id and 
        the user id. 
    Updates the database accordingly.  
        If new status is pending (only when called in ), then ignore task id and user id, update all
        
    Helper function to update assignment status,
    '''
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    if status == "pending":
        query = '''UPDATE assignments INNER JOIN tasks 
                ON assignments.taskID = tasks.id
                SET assignments.status = 'pending', recommendTime = NOW()
                WHERE (assignments.status = 'not assigned' AND tasks.expired != 1)
        '''
        cur.execute(query)
    elif status == "accepted" or status == "rejected":
        cur.execute(f"UPDATE assignments SET `status` = '{status}' WHERE taskID={task_id} AND userID='{user_id}'")
    conn.commit()
    conn.close

def get_assigned_tasks(user_id) -> list:
    """
    Takes a user id (int)
    Finds that user's assignment data.
    
    """
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT taskID FROM assignments 
                WHERE userID = '{user_id}'
            '''
    cur.execute(query)
    task_list = [item[0] for item in cur.fetchall()]
    conn.close()
    return task_list

def submit_task(user_id, task_id, path):
    update_tasks_expired()
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT expired FROM tasks WHERE id = {task_id}")
    expired = cur.fetchone()[0]
    if expired == 0:
        query = f'''UPDATE assignments 
                    INNER JOIN users ON assignments.userID = users.id
                    INNER JOIN tasks ON assignments.taskID = tasks.id
                SET assignments.img = '{path}', assignments.submissionTime = NOW(),
                    users.compensation = users.compensation+ tasks.compensation
                WHERE (assignments.userID = '{user_id}' 
                    AND assignments.taskID = {task_id})
                '''
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
    else:
        return False



if __name__ == "__main__":
    pass

