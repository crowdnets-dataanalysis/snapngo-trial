# code to open text file and read into a matrix
def read_file(fname):
    with open(fname, "r") as file:
        # Read the first line that contains the number of vertices
        numVertices = int(file.readline().strip())

        # Create a dictionary to store each vertex and its corresponding location description
        vertices = {}
        for _ in range(numVertices):
            line = file.readline().strip().split(",")
            vertices[int(line[0])] = line[1]

        # Create an empty matrix
        matrix = [[int(-1) for _ in range(numVertices)] for _ in range(numVertices)]

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
    
if __name__ == '__main__':
    matrix, vertices = read_file("graph.txt")
    print(matrix)
    print(vertices)
