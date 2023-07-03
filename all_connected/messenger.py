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
DB_NAME = "snapngo_db" 


def add_users(user_store):
    '''
    Gets teh database connection. Returns nothing.
    Add users to the database based on the current list of users in the the workplace 
    '''
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    # user_store = get_all_users_info()
    query = '''INSERT IGNORE INTO users (name, id) VALUES (%s, %s)'''
    for key in user_store:
        not_bot = user_store[key]['is_bot'] == False
        not_slackbot = (key != 'USLACKBOT')
        if not_bot and not_slackbot:
            name = user_store[key]['name']
            cur.execute(query, (name, key))
            conn.commit()
    conn.close()

def get_total_users():
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = "SELECT COUNT(id) FROM users WHERE `status` = 'active'"
    cur.execute(query)
    total_users = cur.fetchone()[0]
    return int(total_users)

def get_active_users_list():
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = "SELECT id FROM users WHERE `status` = 'active'"
    cur.execute(query)
    active_users_list = cur.fetchall()
    active_users = [user[0] for user in active_users_list]
    return active_users

def get_account_info(user_id):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f"SELECT compensation FROM users WHERE id = '{user_id}'"
    cur.execute(query)
    compensation = cur.fetchone()[0]
    query = f"SELECT task_id FROM assignments WHERE user_id = '{user_id}' AND checked = 1 AND submission_time IS NOT NULL"
    cur.execute(query)
    tasks = [task[0] for task in cur.fetchall()]
    return compensation, tasks

def update_account_status(user_id, status):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET `status` = '{status}' WHERE id = '{user_id}'")
    conn.commit()
    conn.close


def update_tasks_expired():
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET `expired` = 1 WHERE (start_time + INTERVAL time_window MINUTE) < NOW()")
    conn.commit()
    conn.close

def get_task_list(user_id, task_id):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT assignments.task_id, assignments.user_id, 
                tasks.location, tasks.description, tasks.start_time, tasks.time_window, 
                tasks.compensation
                FROM assignments INNER JOIN tasks ON assignments.task_id = tasks.id
                WHERE (assignments.task_id = {task_id} AND assignments.user_id = '{user_id}')'''
    cur.execute(query)
    assignment = cur.fetchone()
    conn.close()
    assert assignment, f"Assignment #{task_id} could not be found in database!"
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
    query = '''SELECT assignments.task_id, assignments.user_id, 
                tasks.location, tasks.description, tasks.start_time, tasks.time_window, 
                tasks.compensation
                FROM assignments INNER JOIN tasks ON assignments.task_id = tasks.id
                WHERE (assignments.`status` = 'not assigned' AND tasks.expired != 1)'''
    cur.execute(query)
    assignments = cur.fetchall()
    conn.close()
    assignments_dict = {}
    for assignment in assignments:
        uid = assignment[1]
        if uid in assignments_dict:
            (assignments_dict[uid]).append(assignment)
        else:
            assignments_dict[uid] = [assignment]       
    return assignments_dict

def get_assign_status(task, user):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT status FROM assignments
                WHERE task_id = {task} AND user_id = '{user}'
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
                ON assignments.task_id = tasks.id
                SET assignments.`status` = 'pending', recommend_time = NOW()
                WHERE (assignments.`status` = 'not assigned' AND tasks.expired != 1)
        '''
        cur.execute(query)
    elif status == "accepted" or status == "rejected":
        cur.execute(f"UPDATE assignments SET `status` = '{status}' WHERE task_id={task_id} AND user_id='{user_id}'")
    conn.commit()
    conn.close

def get_accepted_tasks(user_id) -> list:
    """
    Takes a user id (int)
    Finds that user's assignment data.
    
    """
    update_tasks_expired()
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT DISTINCT assignments.task_id
                FROM assignments INNER JOIN tasks 
                ON assignments.task_id = tasks.id
                WHERE (assignments.user_id = '{user_id}') AND (assignments.`status` = 'accepted') AND (tasks.expired != 1) AND (img IS NULL)'''
    cur.execute(query)

    task_list = [int(task_id[0]) for task_id in cur.fetchall()]
    
    conn.close()
    return task_list

def get_pending_tasks(user_id) -> list:
    """
    Takes a user id (int)
    Finds that user's assignment data.
    
    """
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    # query = f'''SELECT task_id FROM assignments 
    #             WHERE user_id = '{user_id}' AND `status` = 'pending'
    #         '''
    query = f'''SELECT DISTINCT assignments.task_id 
                FROM assignments INNER JOIN tasks
                ON assignments.task_id = tasks.id
                WHERE assignments.user_id = '{user_id}' AND assignments.`status` = 'pending' AND tasks.expired = 0
            '''
    cur.execute(query)
    task_list = [item[0] for item in cur.fetchall()]
    conn.close()
    return task_list

def check_time_window(task_id):
    update_tasks_expired()
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT expired, (start_time<NOW()) FROM tasks WHERE id = {task_id}")
    timing = cur.fetchone()
    expired = timing[0]
    started = timing[1]
    if expired == 1:
        return "expired"
    elif started == 0:
        return "not started"

def submit_task(user_id, task_id, path):
    update_tasks_expired()
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT expired, (start_time<NOW()) FROM tasks WHERE id = {task_id}")
    timing = cur.fetchone()
    expired = timing[0]
    started = timing[1]
    if expired == 0 and started == 1:
        query = f'''UPDATE assignments 
                    INNER JOIN users ON assignments.user_id = users.id
                    INNER JOIN tasks ON assignments.task_id = tasks.id
                SET assignments.img = '{path}', 
                    assignments.`submission_time` = NOW()
                WHERE (assignments.user_id = '{user_id}' 
                    AND assignments.task_id = {task_id})
                '''
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
    else:
        return False

def delete_submission(user_id, task_id):
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''UPDATE assignments
            SET img = NULL, submission_time = NULL
            WHERE user_id = {user_id} AND task_id = {task_id}
            '''
    cur.execute(query)
    conn.commit()
    return
    
def check_all_assignments():
    conn = helper_functions.connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''UPDATE assignments 
                INNER JOIN users ON assignments.user_id = users.id
                INNER JOIN tasks ON assignments.task_id = tasks.id
            SET users.compensation = users.compensation+ tasks.compensation,
                assignments.checked = 1
            WHERE (assignments.checked = 0 AND submission_time IS NOT NULL)
            '''
    cur.execute(query)
    conn.commit()
    return

if __name__ == "__main__":
    pass

