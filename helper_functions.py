import networkx as nx
from heapq import*

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
            p.append(sum / client.k)
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


### Remote all the bots home when all L bots are found
# Based on MST
# This function should be used after all bots are found
# Finished but UNTESTED, correctness unknown
def remoteKnownBotHome(client):
    knownBots = [client.h]
    for i in range(client.v):
        if (client.bot_count[i] > 0):
            knownBots.append(i)
    newG = nx.Graph()
    for i in range(len(knownBots)):
        newG.add_node(knownBots[i])
    for (u, v, wt) in client.G.edges.data('weight'):
        if u in knownBots and v in knownBots:
            newG.add_edge(u, v, weight = wt)

    MST = nx.minimum_spanning_tree(newG)
    bfs_edge = list(nx.edge_bfs(MST, source = client.home))

    for edge in bfs_edge:
        client.remote(edge[1], edge[0])



### Find all the l bots based on the vote of the students.
# We want to check what is students' possibility to make a mistake
# Unfinished
def findAllBots(client):
    vote = votes(client)
    

### Return the shortest path
# based on dijkstra
def shortestPathfromHome(client):
    SP = nx.single_source_shortest_path(client.G, client.h)
    return SP


### Remote from a specific vertex to home along shortest path
# Input
# Return # of bots actually gets home
# Based on dijkstra
# Unfinished
def remoteHome(client, shortestPaths, vertex):
    path = shortestPaths[vertex]
    path = path[::-1]
    r = 0
    for i in range(len(path) - 1):
        r = client.remote(path[i], path[i + 1])
    return r