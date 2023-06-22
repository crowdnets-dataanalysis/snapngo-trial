"""
Name: Sofia Kobayashi
Date: 06/07/2023
Description: General helper functions & environment set up for the overall Snap N Go connections.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

import pymysql
from flask import Flask
from threading import Timer

from datetime import datetime, time

START_HOURS = time(10,00)
END_HOURS = time(16,00)

def connectDB(dbName):
    """
     * General Helper Function * 
    Takes a database name (str).
    Returns a connection object to that database. This connection should eventually
        be closed with .close()
    """
    # Connect to the database
    db = pymysql.connect(
        host='localhost',
        user='root', 
        password=os.environ['SQL_PASS'], 
        db=dbName
    )

    return db


# code to open text file and read into a matrix
def read_file(fname):
    with open(fname, "r") as file:
        # Read the first line that contains the number of vertices
        numVertices = int(file.readline().strip())

        # Create a dictionary to store each vertex and its corresponding location description
        vertices = {}
        for _ in range(numVertices):
            line = file.readline().strip().split(",")
            vertices[line[0]] = line[1]

        # Create an empty matrix
        matrix = [[-1 for _ in range(numVertices)] for _ in range(numVertices)]

        # Next, read the edges and build the graph
        for line in file:
            # edge is a list of 3 values representing a pair of adjacent vertices and their distance
            edge = line.strip().split(",")
            v1, v2, distance = int(edge[0]), int(edge[1]), float(edge[2])

            # Update the matrix with the distance between v1 and v2
            matrix[v1-1][v2-1] = distance
            matrix[v2-1][v1-1] = distance

        # Return the matrix and the dictionary of vertices
        return matrix, vertices

class RepeatTimer(Timer):
    def __init__(self, func, seconds=10, minutes=0, hours=0):
        super().__init__(seconds + minutes*60 + hours*3600, func)
        func()

    def run(self):
        now = datetime.now()
        not_weekend = now.strftime("%A").lower() not in {'saturday', 'sunday'}
        during_workday = START_HOURS < now.time() < END_HOURS
        while not self.finished.wait(self.interval) and not_weekend and during_workday:
            self.function(*self.args, **self.kwargs)


if __name__ == '__main__':
    pass