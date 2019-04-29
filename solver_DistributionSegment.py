import networkx as nx


# python local_server.py
# python client.py --solver solver_DistributionSegment
# python runSolverManyTimes.py
# average score: 91.701294253001

# invariants:
#   the vertices are always processed in order of decreasing probability segments
#   within each segment, the vertices are always processed in order of increasing distance

def solve(client):
    client.start()
    vote_array = votes(client)

    # grab the distribution, find probabilities by client.k
    distribution = {}
    for vertex, vote in enumerate(vote_array):
        if vote not in distribution.keys():
            distribution[vote] = []
        distribution[vote].append(vertex)

    vertex_100_to_70 = []
    vertex_70_to_50 = []
    vertex_50_to_30 = []
    vertex_30_to_0 = []

    # segmentation of vertices based on student votes
    for vote in sorted(distribution):
        if vote >= 0.7 * client.k:
            vertex_100_to_70.extend(distribution[vote])
        elif vote >= 0.5 * client.k:
            vertex_70_to_50.extend(distribution[vote])
        elif vote >= 0.3 * client.k:
            vertex_50_to_30.extend(distribution[vote])
        else:
            vertex_30_to_0.extend(distribution[vote])

    segments = [vertex_100_to_70, vertex_70_to_50, vertex_50_to_30, vertex_30_to_0]

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
        segment.sort(key=lambda v: shortest_path_length[v + 1])

    # remote based on predefined ordering until we find all bots
    counter = 0
    for segment in segments:
        if segment == vertex_70_to_50:
            print("Touched segments below 70% probability")
        if segment == vertex_50_to_30:
            print("Touched segments below 50% probability")
        if segment == vertex_30_to_0:
            print("Touched segments below 30% probability")
        for vertex in segment:
            counter += remote_home(client, shortest_path, vertex + 1)
            if counter == client.l:
                score = client.end()
                return score


def votes(client):
    vote_array = []
    for v in range(client.v):
        if v + 1 == client.h:
            vote_array.append(0)
        else:
            results = client.scout(v + 1, list(range(1, client.k + 1)))
            sum = 0
            for s in range(client.k):
                if results[s + 1]:
                    sum += 1
            vote_array.append(sum)
    return vote_array


def remote_home(client, shortest_paths, vertex):
    path = shortest_paths[vertex]
    path = path[::-1]
    action = 0
    for e in range(len(path) - 1):
        action = client.remote(path[e], path[e + 1])
    return action
