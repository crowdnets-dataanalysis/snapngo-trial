import random
import pymysql
import loadGraph

def connectDB(dbName):

    # Connect to the database
    db = pymysql.connect(
        host='localhost',
        user='root', 
        password='password', # edit
        db=dbName
    )

    return db

def insertTasks(numTasks):
    # Connect to database
    db = connectDB('snapngo_db');

    # Create a cursor object
    cursor = db.cursor()

    # Get matrix representation of graph and dictionary of vertex indices and location descriptions
    matrix, vertices = loadGraph.read_file("graph.txt")

    for i in range(numTasks):
        # Insert the vertex and time into the database
        query = "INSERT INTO Tasks(location, time) VALUES (%s, %s)"
        values = createTask(vertices)
        cursor.execute(query, values)
        # Commit the changes to the database
        db.commit()

    # Close the database connection
    db.close()

def createTask(vertices):
    # Generate a random vertex number and time
    vertex = random.randint(1, len(vertices))
    time = random.randint(1, 100)

    # Return location description and time
    return vertices[vertex], time

    
if __name__ == '__main__':
    insertTasks(3)