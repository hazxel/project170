import networkx as nx
from helper_functions import *


# python local_server.py
# python client.py --solver solver_CandidateMerging
# python runSolverManyTimes.py
# average score: 91.79336560472193

# invariants:
#   the candidates list always contains client.l - counter candidates
#   the candidates list is always sorted in increasing distance from home in same segment
#   the candidates list never touches vertices with less than 50% probability


def solve(client):
    client.end()
    client.start()
    vote_array = votes(client)

    # sort the vertices based on student votes
    vertices = list(range(client.v))
    vertices.sort(key=lambda v: vote_array[v])
    vertices.reverse()

    # calculate the length of shortest path from each vertex to home
    shortest_path_to_home = nx.single_source_shortest_path(client.G, client.h)
    shortest_path_to_home_length = {}

    for vertex in sorted(shortest_path_to_home):
        distance = 0
        path = shortest_path_to_home[vertex]
        for e in range(len(path) - 1):
            distance += client.G.edges[path[e], path[e + 1]]['weight']
        shortest_path_to_home_length[vertex] = distance

    # maintain a candidates list of length bots_left
    counter = 0
    vertex_index = 0
    candidates = []
    while counter < client.l:
        # at the start of loop always refill candidates
        for _ in range(client.l - counter - len(candidates)):
            candidates.append(vertices[vertex_index] + 1)
            vertex_index += 1

        # potential target vertex is the one closest to home
        target = min(candidates, key=lambda c: shortest_path_to_home_length[c])
        bots_moved_to_target = 0

        # calculate distance to target from each candidate
        shortest_path_to_target = nx.single_source_shortest_path(client.G, target)
        shortest_path_to_target_length = {}
        for candidate in candidates:
            distance = 0
            path = shortest_path_to_target[candidate]
            for e in range(len(path) - 1):
                distance += client.G.edges[path[e], path[e + 1]]['weight']
            shortest_path_to_target_length[candidate] = distance

        # remote each candidate to target or home depending on distance
        for candidate in candidates:
            if candidate == target:
                continue
            if shortest_path_to_target_length[candidate] < shortest_path_to_home_length[candidate]:
                bots_moved_to_target += remoteHome(client, shortest_path_to_target, candidate)
                candidates.remove(candidate)
            else:
                counter += remoteHome(client, shortest_path_to_home, candidate)
                candidates.remove(candidate)

        # finally remote from target to home, potentially carrying many bots
        counter += remoteHome(client, shortest_path_to_home, target)
        candidates.remove(target)

    score = client.end()
    return score