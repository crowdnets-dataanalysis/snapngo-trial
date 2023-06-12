"""
terminal command to get into SQL:
source .bash_profile
mysql -u root -p
to get slack running:
ngrok http 5000 (in one terminal)
run this file in another terminal
(both of these things need to happen in order to run )
"""
import os
import bot
import helper_functions
from pathlib import Path
from dotenv import load_dotenv
import pymysql
from slack_sdk import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
# setting up .env path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Create flask app
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['CAT_BOT_SIGNING_SECRET'], '/slack/events', app)

# Define the client obj
client = WebClient(token=os.environ['CAT_BOT_TOKEN'])
# Get the bot id
BOT_ID = client.api_call("auth.test")['user_id']



def getAllUsersInfo():
    return bot.getAllUsersInfo()

def addUsers(conn):
    '''
    Gets teh database connection. Returns nothing.
    Add users to the database based on the current list of users in the the workplace 
    '''
    cur = conn.cursor()
    user_store = getAllUsersInfo()
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
    

def getAssignments(db_name):
    '''
    Get all the assignments with status 'not assigned' together with each task's details. 
    Create a dictionary with keys being user ids and values being a list of tasks (with
    details) that user is assigned
    Return the dictionary
    '''
    conn = helper_functions.connectDB(db_name)
    cur = conn.cursor()
    cur.execute(f"UPDATE tasks SET expired = 1 WHERE starttime + INTERVAL time_window minute < now()")
    query = '''SELECT assignments.taskID, assignments.userID, 
                tasks.location, tasks.description, tasks.starttime, tasks.time_window, 
                tasks.compensation
                FROM assignments INNER JOIN tasks ON assignments.taskID = tasks.id
                WHERE assignments.status = 'not assigned' AND tasks.expired != 1;'''
    cur.execute(query)
    assignments = cur.fetchall()
    assignmentsDict = {}
    for assign in assignments:
        uid = assign[1]
        #print(uid)
        if uid in assignmentsDict:
            (assignmentsDict[uid]).append(assign)
        else:
            assignmentsDict[uid] = [assign]
    conn.close()        
    #print(assignmentsDict)
    return assignmentsDict

if __name__ == "__main__":
    #addUsers()
    assignDict = getAssignments('test1')
    bot.sendTasks(assignDict)
