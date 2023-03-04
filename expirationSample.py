# sample code for checking task expiration?
# assuming tasks are given as tuples in the format (task, location, submit time, range)
# submit time is the time when the task should be submitted and range is the amount of time before and after the submit time when the user can submit the task

import time


def findIndex(stack, task, index):
    index = len(stack)
    start = time.time()
    # updating task expiration time
    lst = list(task)
    lst[2] += start
    task = tuple(lst)
    # Searching for the position
    for i in range(len(stack)):
        if stack[i][index] > task[index]:
            index = i
            return index
    return index


def addTask(stack, task, index):
    idx = findIndex(stack, task, index)

    # Inserting n in the list
    if idx == len(stack):
        stack.append(task)
    else:
        stack = stack[:idx] + [task] + stack[idx:]
    return stack


def checkStart(stack):
    startList = []
    while len(stack) > 0 and stack[0][2] > time.time():
          startList.append(stack.pop(0))
    return stack, startList


def checkExpiration(stack):
    expiredList = []
    while len(stack) > 0 and stack[0][3] > time.time():
          startList.append(stack.pop(0))
    return stack, expiredList


if __name__ == '__main__':
    # sample task list [("task1", "loc1", time.time(), 100),("task1", "loc1", time.time(), 300),("task1", "loc1", time.time(), 500)]
    initial = time.time() + 2000
    print(initial)
    #stack designed to include task information and start + end time, sorted by which starts submission first
    startStack = [("task1", "loc1", initial - 500, initial + 500), ("task2", "loc2", initial - 300, initial + 300), ("task3", "loc3", initial - 100, initial + 100)]

    #stack designed to include task information and start + end time, sorted by which end submission first
    endStack = []

    newTask = ("newTask", "newLoc", time.time(), 400)
    stack = addTask(startStack, newTask, 2)  # add a new task to the start stack
    #print(stack)

    while len(startStack) > 0 and len(endStack)>0:  # just waiting until all stacks are empty right now but could be changed to be checked depending on other code
        startStack, startList = checkStart(stack)
        for x in startList:
          endStack = addTask(endStack, x, 3) #add all started tasks to the list of tasks to look at expiry 
        
        endStack, expiredList = checkExpiration(endStack) #checking active tasks for expiration
        
        if len(expiredList) > 0:
            print(time.time())
            print(endStack)#print new list of active tasks
