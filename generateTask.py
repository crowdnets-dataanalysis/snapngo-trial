import random
import pymysql

def insertTask():

    # Connect to the database
    db = pymysql.connect(
        host='localhost',
        user='root', 
        password='password', # edit
        db='snapngo_db'
    )

    # Create a cursor object
    cursor = db.cursor()

    # Generate a random vertex number and time
    vertex = random.randint(1, 20)
    time = random.randint(1, 100)

    # Insert the vertex and time into the database
    query = "INSERT INTO tasks(vertex, time) VALUES (%s, %s)"
    values = (vertex, time)
    cursor.execute(query, values)

    # Commit the changes to the database
    db.commit()

    # Close the database connection
    db.close()

if __name__ == '__main__':
    insertTask()