### Returns a list which shows the number of students who believe there exists a bot on a certain vertex.
### Be careful that this function runs client.scout() k*v times.
def votes(client):
    p = []
    vertices = list(range(1, client.v + 1))
    students = list(range(1, client.students + 1))
    for i in range(client.v):
        if (vertices[i] == client.home):
            p.append(0)
        else:
            dict = client.scout(vertices[i], students)
            sum = 0
            for std in students:
                if dict[std] == True:
                    sum = sum + 1
            p.append(sum)
    return p


### Returns a list which shows the proportion of students who believe there exists a bot on a certain vertex.
### Be careful that this function runs client.scout() k*v times.
def probability(client):
    p = []
    vertices = list(range(1, client.v + 1))
    students = list(range(1, client.students + 1))
    for i in range(client.v):
        if (vertices[i] == client.home):
            p.append(0)
        else:
            dict = client.scout(vertices[i], students)
            sum = 0
            for std in students:
                if dict[std] == True:
                    sum = sum + 1
            p.append(sum)
    return p



### Print some information about the graph, including:
# Home vertex
# Numer of Student
# Number of bots
# Number of vertices
# Number of edges
def printGraphInfo(client):
    print("Information about the city:")
    # print("    Home vertex: ", client.h)
    # print("    Number of students: ", client.k)
    # print("    Number of bots: ", client.l)
    print("    Number of vertices: ", client.v)
    print("    Number of edges: ", client.e)

    '''
    ### Uncomment this if you want to check every sigle edge
    print("All the edges are:")
    for (u, v, wt) in client.G.edges.data('weight'):
        print('(%d, %d, %.3f)' % (u, v, wt))
    '''