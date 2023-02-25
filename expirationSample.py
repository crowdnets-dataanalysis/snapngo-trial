#sample code for checking task expiration?
#assuming tasks are given as tuples in the format (task, location, expiration time) and that expiration time is the amount of time after the task is added before expiration
import time

def addTask(stack, task):
    index = len(stack)
    start = time.time()
    #updating task expiration time
    lst = list(task)
    lst[2] = lst[2]+start
    task = tuple(lst)
    # Searching for the position
    for i in range(len(stack)):
      if stack[i][2] > task[2]:
        index = i
        break
 
    # Inserting n in the list
    if index == len(stack):
      stack = stack[:index] + [task]
    else:
      stack = stack[:index] + [task] + stack[index:]
    return stack


def checkExpiration(stack):
    expiredList = []
    if len(stack)>0 and stack[0][2]<time.time():
       while len(stack)>0 and stack[0][2]<time.time():
          expiredList.append(stack.pop(0))
    return stack, expiredList

if __name__ == '__main__':
    #sample task list [("task1", "loc1", 100),("task1", "loc1", 300),("task1", "loc1", 500)]
    initial = time.time()
    print(initial)
    stack = [("task1", "loc1", initial + 10),("task2", "loc2", initial + 30),("task3", "loc3", initial + 50)]
    newTask = ("newTask", "newLoc", 40)
    stack = addTask(stack, newTask) #add a new task to the stack
    print(stack)

    while len(stack)>0: #just waiting until stack is empty right now but could be changed to be checked depending on other code
       stack, expiredList = checkExpiration(stack)
       if len(expiredList) > 0:
          print(time.time())
          print(stack)