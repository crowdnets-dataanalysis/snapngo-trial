#code to open text file and read into a matrix
def read_file(fname):
    # Open the file
    file = open(fname, "r")
    # Read the first line that contains the number of vertices
    # numVertices is the number of vertices in the graph (n)
    numVertices = int(file.readline())

    #read the next numVertices lines which contain the vertex number and the actual location
    #dictionary is all of the verticies and their values
    dictionary = {}
    for x in range(20):
        line = file.readline().strip().split(",")
        dictionary[line[0]]= line[1]
    #make matrix
    matrix = [[-1 for i in range (numVertices)]for i in range (numVertices)]
    # Next, read the edges and build the graph
    for line in file:
        # edge is a list of 2 indices representing a pair of adjacent vertices
        # edge[0] contains the first vertex (index between 0 and numVertices-1)
        # edge[1] contains the second vertex (index between 0 and numVertices-1)
        edge = line.strip().split(",")
        matrix[int(edge[0])-1][int(edge[1])-1]= edge[2]
        matrix[int(edge[1])-1][int(edge[0])-1]= edge[2]
        print(matrix)
    # Use the edge information to populate your adjacency list
    
    # Close the file safely after done reading
    file.close()

if __name__ == '__main__':
    matrix = read_file("graph.txt")