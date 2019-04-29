import networkx as nx
import numpy as np
import math


### Returns a list which stores all the information we get from scout()
### Be careful that this function runs client.scout() k*v times.
# Input: -
# Output: A list showing the number of students who believe there exists a bot on a certain vertex.
def votes(client, num_students_samples=None):
    p = []
    vertices = list(range(1, client.v + 1))
    # Number of students we use
    if not num_students_samples or num_students_samples >= client.students:
        students = list(range(1, client.students + 1))
    else:
        print("Number of students used:", num_students_samples)
        students = np.random.choice(np.arange(1, client.students + 1), num_students_samples, replace=False).tolist()
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


### Returns a list which shows the probability of bots' existance on a certain vertex.
### Be careful that this function runs client.scout() k*v times.
### Very similar to votes()
# Input: -
# Output: A list showing the proportion of students who believe there exists a bot on a certain vertex.
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

### Computes the average edge weights
def averageEdgeWeight(client):
    average_EW = 0
    print("    Number of edges: ", client.e)
    for (_, _, wt) in client.G.edges.data('weight'):
        average_EW += wt/client.e

    print("    Average Edge weights: ", average_EW)
    return average_EW

### Computes the average edge weights/number of vertices ratio
def averageEdgeWeight_numOfVertices(client):
    print("    Number of vertices: ", client.v)
    return averageEdgeWeight(client) / client.v


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
            newG.add_edge(u, v, weight=wt)

    MST = nx.minimum_spanning_tree(newG)
    bfs_edge = list(nx.edge_bfs(MST, source=client.home))

    for edge in bfs_edge:
        client.remote(edge[1], edge[0])


### Return the shortest path
# based on dijkstra
# Untested
def shortestPathfromHome(client):
    SP = nx.single_source_shortest_path(client.G, client.h)
    return SP


### Remote from a specific vertex to home along shortest path
### Based on dijkstra
### Correctness guaranteed
# Input: a list of shortest paths with home as single source
#        a vertex we want to remote home from
# Return: number of bots actually got home

def remoteHome(client, shortestPaths, vertex):
    path = shortestPaths[vertex]
    path = path[::-1]
    r = 0
    for i in range(len(path) - 1):
        r = client.remote(path[i], path[i + 1])
    return r


### Estimate the accuracy of scout()
### Based on the variance and distribution of vote()
### Assume that accuracy is always larger than 50%
# Input: a list of vote info
# Output: Overall statistical estimation of accuracy of scout
# Unfinished
def estimatedAccuracy(client, vote):
    stdNum = client.k
    vNum = client.v
    botNum = client.l

    # if students are 100% correct:
    # correctVoteNum = vNum * stdNum
    actualVoteNum = sum(vote)

    # Say that students' accuracy is p
    # Then on every vertex we have a bot, we get approximately k * p votes
    # And for each vertex doesn't exist a bot, we get approximately k * (1 - p) votes
    # So overall expected votes should be l * k * p + (v - l) * k * (1 - p) = (2 * l - v) * k * p + (v - l) * k
    # So, estemated p = (SumOfVote - (v - 1) * k) / ((2 * l - v) * k)

    p = (actualVoteNum - (vNum - botNum) * stdNum) / ((botNum - vNum + botNum) * stdNum)
    return p


### Print the distribution of vote
# Input: list of vote
# Output: -
def printVote(vote):
    stat = {}
    for i, vo in enumerate(vote):
        if vo not in stat.keys():
            stat[vo] = []
        stat[vo].append(i + 1)
    print('Votes distribution:')
    for j in sorted(stat):
        print("    votes: {}, vertices {}".format(j, stat[j]))


### Calculate the probability of bots' existance on the vertex
# Use the overall students' accuracy to estimate the correctness of a certain vertex
def calCorrectProb(client, vote, accuracy, vertex):
    vertex = vertex - 1
    rightProb = math.factorial(client.k) / math.factorial(client.k - vote[vertex]) / math.factorial(
        vote[vertex]) * accuracy ** vote[vertex] * (1 - accuracy) ** (client.k - vote[vertex])
    leftProb = math.factorial(client.k) / math.factorial(client.k - vote[vertex]) / math.factorial(
        vote[vertex]) * (1 - accuracy) ** vote[vertex] * accuracy ** (client.k - vote[vertex])
    prob = rightProb / (rightProb + leftProb)
    return prob
