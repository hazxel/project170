import networkx as nx
import numpy as np
import random
from helper_functions import *

'''
To test locally, please do the following:

    Run the local server using "python local_server.py“ in terminal.

    This will start a web server that your client will now connect to. It will pick a random input instance to serve. 
    An instance is a set of parameters (such as bot locations or student correctness) of the problem.

    In a separate terminal, run "python client.py --solver solver". The --solver flag indicates the solver python file 
    the client should use. It's the file name of your solver, with .py omitted.

    If you want to try a different solver run "python client.py --solver <MY_SOLVER_NAME>"

    In both terminals, you should see a slew of scout and remote calls succeeding. At the bottom of the client terminal 
    your score is shown. The score should be very low (since it's unlikely all bots were moved home).
'''


# average score: 91.25701361131173


def solve(client):
    client.end()
    client.start()
    vote_raw = votes(client)
    vote_array = np.array(vote_raw)

    # grab the distribution, find probabilities by client.k
    distribution = {}
    for vertex, vote in enumerate(vote_array):
        if vote not in distribution.keys():
            distribution[vote] = []
        distribution[vote].append(vertex)

    vertex_above_70 = []
    vertex_above_50 = []
    vertex_above_30 = []
    vertex_below_30 = []

    # segmentation of vertices based on student votes
    for vote in sorted(distribution):
        if vote >= 0.7 * client.k:
            vertex_above_70.extend(distribution[vote])
        elif vote >= 0.5 * client.k:
            vertex_above_50.extend(distribution[vote])
        elif vote >= 0.3 * client.k:
            vertex_above_30.extend(distribution[vote])
        else:
            vertex_below_30.extend(distribution[vote])

    segments = [vertex_above_70, vertex_above_50, vertex_above_30, vertex_below_30]

    # reorder each segment based on shortest path distance from home
    shortest_path = nx.single_source_shortest_path(client.G, client.h)
    shortest_path_length = {}

    for vertex in sorted(shortest_path):
        distance = 0
        path = shortest_path[vertex]
        for e in range(len(path) - 1):
            distance += client.G.edges[path[e], path[e + 1]]['weight']
        shortest_path_length[vertex] = distance

    for segment in segments:
        segment.sort(key=lambda v: shortest_path_length[v+1])

    # remote based on predefined ordering until we find all bots
    counter = 0
    for segment in segments:
        if counter == client.l:
            break
        if segment == vertex_above_30:
            print("Touched segments below 50% probability")
        if segment == vertex_below_30:
            print("Touched segments below 30% probability")
        for vertex in segment:
            if counter == client.l:
                break
            counter = counter + remoteHome(client, shortestPathfromHome(client), vertex + 1)

    score = client.end()
    # print("The input was: V", client.v, " E: ", client.e, " L: ", client.l, " K: ", client.k)
    return score
