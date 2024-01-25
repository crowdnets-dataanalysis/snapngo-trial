from datetime import datetime, time
import random

import matching_assignments
import messenger

num_total_users = messenger.get_total_users() #get number of total participants from the database
                                                #helper variable

##### TASK CYCLE PARAMETERS #####
START_HOURS = time(9,00) #9 am
END_HOURS = time(17,00) #5:00 pm


TASK_CYCLE = 30*60      #in seconds. cycle where new tasks are generated. 
                        #Default: every 30 minutes
NUM_TASKS_PER_CYCLE = num_total_users   #number of tasks generated per cycle
                                        #Default: one task per person every cycle. 
                                        #i.e. everyone receives on average two tasks per hour


MATCHING_CYCLE = TASK_CYCLE+2   #in seconds. cycle where tasks are matched with users
                                #Default: 2 seconds longer than task generation cycle. 
                                    #Making sure all tasks are generated before we match them with users.

MESSENGER_BOT_CYCLE = 60*60+2   #in seconds. cycle where the slack bot send the assigned tasks to each user.
                                #Default: 1 hour and 2 seconds.
                                    #Again, making sure all tasks are matched before we send them to users.



TASK_TIMEWINDOW = random.randint(1, 100) #in minutes. the length of time allowed for finishing one task
                                            #Default: from 1 minute to 100 minutes.
TASK_COMP = random.randint(2, 5) #in points. the compensation participants can get for finishing each task
                                    #Default: from 2 to 5 points


##### #####
MATCHING_ALGO = matching_assignments.algorithm_random   #random matching algorithm
# MATCHING_ALGO = matching_assignments.algorithm_weighted   #weighted random matching algorithm


##### #####
admin_list = ["U05BL0N0G5V", "U05B24S3LR9"] #system admins (eg. researchers) can put their slack ID in this list
                                            #if they don't wish to receive tasks like users do.
