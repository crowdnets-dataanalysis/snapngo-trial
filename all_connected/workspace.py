import copy
import random
import json
from datetime import datetime, timedelta

import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

from messenger import update_tasks_expired, get_task_list
from helper_functions import connectDB

DB_NAME = os.environ['DB_NAME']


with open('block_messages/default_btn.json', 'r') as infile:
    default_btn = json.load(infile)

with open('block_messages/headers.json', 'r') as infile:
    block_headers = json.load(infile)


def get_accepted_tasks(user_id) -> list:
    """
    Takes a user id (int)
    Finds that user's assignment data.
    
    """
    update_tasks_expired()
    conn = connectDB(DB_NAME)
    cur = conn.cursor()
    query = f'''SELECT DISTINCT assignments.task_id
                FROM assignments INNER JOIN tasks
                WHERE assignments.user_id = '{user_id}' AND assignments.`status` = 'accepted' AND tasks.expired = 0 AND img IS NULL'''
    cur.execute(query)

    task_list = [int(task_id[0]) for task_id in cur.fetchall()]
    
    conn.close()
    return task_list


def get_pending_tasks(user_id) -> list:
    """
    Takes a user id (int)
    Finds that user's assignment data.
    
    """
    conn = connectDB(DB_NAME)
    cur = conn.cursor()
    # query = f'''SELECT task_id FROM assignments 
    #             WHERE user_id = '{user_id}' AND `status` = 'pending'
    #         '''
    query = f'''SELECT DISTINCT assignments.task_id 
                FROM assignments INNER JOIN tasks
                WHERE assignments.user_id = '{user_id}' AND assignments.`status` = 'pending' AND tasks.expired = 0
            '''
    cur.execute(query)
    task_list = [item[0] for item in cur.fetchall()]
    conn.close()
    return task_list


def compact_task(task_info) -> dict:
    """
    Takes a task_info list.
    Formats that task info into a compact task block (for uses outside 
        of when a task is first send to a user).
    Returns a fully formed 'section' Slack block (dict).
    """
    print(task_info)
    starttime_format = task_info[4].strftime("%A (%m/%d) at %I:%M%p")
    text  = "*Task #PLACEHOLDER_TASKID* (*comp:* $PLACEHOLDER_COMPENSATION)\n *Starts:* PLACEHOLDER_STARTTIME, *window*: PLACEHOLDER_WINDOW min \n*Description:* PLACEHOLDER_DESCRIPTION." \
                .replace('PLACEHOLDER_TASKID', str(task_info[0])) \
                .replace('PLACEHOLDER_DESCRIPTION', str(task_info[3])) \
                .replace('PLACEHOLDER_STARTTIME', str(starttime_format)) \
                .replace('PLACEHOLDER_WINDOW', str(task_info[5])) \
                .replace('PLACEHOLDER_COMPENSATION', str(task_info[6])) 
    return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text
			}
		}
    
def make_report_block(user_id) -> list:
    """
    Takes a user id (int? str?)
    Formats a report block for the given user using their 
        active (accepted, unexpired, uncompleted) & 
        pending (pending, unexpired) tasks.
    Returns a full formatted Slack block message (dict).
    
    """
    # A list of task_list lists for all accepted, unexpired, uncompleted tasks
    active_ids = get_accepted_tasks(user_id)
    all_active = [get_task_list(user_id, task_id) for task_id in active_ids]
  
    # A list of task_list lists for all pending & unexpired tasks
    pending_ids = get_pending_tasks(user_id)
    all_pending = [get_task_list(user_id, task_id) for task_id in pending_ids]

    # Add appropriate active task information
    blocks = []
    if all_active:
        if len(blocks) >= 46:
                blocks.append(block_headers['too_many_pending_header'])
        blocks.append(block_headers['active_header'])
        blocks.append(block_headers['divider'])
        
        # Sort active tasks by start time
        sorted_active = sorted(all_active, key=lambda task_list: task_list[4]) 
        for task_list in sorted_active:
            active_task = compact_task(task_list)
            blocks.append(active_task)
    else:
        blocks.append(block_headers['no_active_header'])

    blocks.append(block_headers['divider'])
    
    # Add appropriate pending task information
    if all_pending:
        blocks.append(block_headers['pending_header'])
        
        # Sort pending tasks by start time
        sorted_pending = sorted(all_pending, key=lambda task_list: task_list[4])
        for task_list in sorted_pending:
            if len(blocks) >= 47:
                blocks.append(block_headers['too_many_pending_header'])
                break
            pending_task = compact_task(task_list)
            blocks.append(pending_task)

            buttons = copy.deepcopy(default_btn)
            buttons['block_id'] = str(task_list[0])
            blocks.append(buttons)
    else:
        blocks.append(block_headers['no_pending_header'])

    # Add 'for more info' ending
    blocks.append(block_headers['divider'])
    blocks.append(block_headers['ending_block'])

    return blocks

    

def generate_message(task_info, user_id):
    '''
    Helper function for sendTasks.
    Get the list of task assigned to a user and format them into a 
    json block message.
    Return the block message
    '''
    block = []
    starttime_format = task_info[4].strftime("%A (%m/%d) at %I:%M%p")
    # text = (f"*Task # {task_info[0]}*,Location: {task_info[2]} \n" + 
    #         f"Description: {task_info[3]}\nStart Time: {starttime_format} \n" + 
    #         f"Window: {task_info[5]} minutes \nCompensation: ${task_info[6]}")
    
    emoji_dict = {0: '🪴', 
                  1: '🌺', 
                  2: '🍀', 
                  3: '✨',
                  4: '🐨', 
                  5: '🐶',
                  6: '🐱',
                  7: '🦔',
                  8: '🐱',
                  9: '🪴', 
    }


    text = (f"PLACEHOLDER_EMOJI *Task #PLACEHOLDER_TASKID* PLACEHOLDER_EMOJI \n*Description:* PLACEHOLDER_DESCRIPTION. \n*Start Time:* PLACEHOLDER_STARTTIME \n*Window:* PLACEHOLDER_WINDOW minutes \n*Compensation:* $PLACEHOLDER_COMPENSATION")\
                .replace('PLACEHOLDER_EMOJI', emoji_dict[int(task_info[0][-1])]) \
                .replace('PLACEHOLDER_TASKID', str(task_info[0])) \
                .replace('PLACEHOLDER_DESCRIPTION', str(task_info[3])) \
                .replace('PLACEHOLDER_STARTTIME', str(starttime_format)) \
                .replace('PLACEHOLDER_WINDOW', str(task_info[5])) \
                .replace('PLACEHOLDER_COMPENSATION', str(task_info[6])) 
    description = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
    }
    buttons = button_color(task_info[0], user_id)
    block.append(description)
    block.append(buttons)
    return block

def button_color(task_id, user_id):
    """
    Takes a task id (int) and user id (str).
    Determines button formatting based on assignment status 
    Returns button block.
    """
    status = 'rejected'
    if status == "rejected": # Reject btn is red
        block = copy.deepcopy(default_btn)
        block['elements'][1]['style'] = 'danger'
        block['block_id'] = str(task_id)
    elif status == "accepted": # Accept btn is green
        print('accepted')
        block = copy.deepcopy(default_btn)
        block['elements'][0]['style'] = 'primary'
        block['block_id'] = str(task_id)
    else: # both buttons grey
        block = copy.deepcopy(default_btn)
        block['block_id'] = str(task_id)
    return block





if __name__ == '__main__':
    # task_info = ['268','','','At W118 in the Science Center, take a picture of the door only in the upper half of the photo',datetime.now(),'45', 0.58]
    # user_id = 0
    # res = generate_message(task_info, user_id)
    # res = compact_task(task_info)
    # print(res)

    # res = make_report_block(3)
    res = make_report_block("U05BRV5FE7J")
    print(res)