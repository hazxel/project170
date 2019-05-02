import networkx as nx


# python local_server.py
# python client.py --solver solver_Combination
# python runSolverManyTimes.py
# average score:

def solve(client):
    """
    three stage ultimate solver:
       1) segment the vertices based on vote distribution, sort each segment by distance to home
       2) in early segments, perform local merging within candidates list, taking advantage of high probability
       3) in late segments, minimize info cost by remoting to nearest neighbor to find bots before remoting home
    """
    client.start()

    # Stage 0
    # Distribution Segmentation
    # invariants:
    #   the vertices are always processed in order of decreasing probability segments
    #   within each segment, the vertices are always processed in order of increasing distance

    vote_array = votes(client)

    # grab the distribution, find probabilities by client.k
    distribution = {}
    for vertex, vote in enumerate(vote_array):
        if vote not in distribution.keys():
            distribution[vote] = []
        distribution[vote].append(vertex + 1)

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
    shortest_path_to_home = nx.single_source_shortest_path(client.G, client.h)
    shortest_path_to_home_length = {}

    for vertex in sorted(shortest_path_to_home):
        distance = 0
        path = shortest_path_to_home[vertex]
        for e in range(len(path) - 1):
            distance += client.G.edges[path[e], path[e + 1]]['weight']
        shortest_path_to_home_length[vertex] = distance

    for segment in segments:
        segment.sort(key=lambda v: shortest_path_to_home_length[v])

    # Stage 1
    # Candidate Merging
    # invariants:
    #   the candidates list always contains client.l - counter candidates
    #   the candidates list never touches vertices with less than 50% probability

    print("Started Stage 1")

    counter = 0
    for segment in segments[0:2]:
        vertex_index = 0
        while counter < client.l:
            # if we run out of vertices, move on to next segment
            if vertex_index >= len(segment):
                break

            # at the start of loop reset and fill candidates list
            candidates = []
            while len(candidates) < client.l - counter and vertex_index < len(segment):
                candidates.append(segment[vertex_index])
                vertex_index += 1

            # target vertex is the one closest to home among candidates
            target = min(candidates, key=lambda c: shortest_path_to_home_length[c])

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
                    remote_path(client, shortest_path_to_target, candidate)
                else:
                    counter += remote_path(client, shortest_path_to_home, candidate)
                    if counter == client.l:
                        score = client.end()
                        return score

            # finally remote from target to home, potentially carrying many bots
            counter += remote_path(client, shortest_path_to_home, target)
            if counter == client.l:
                score = client.end()
                return score

    # Stage 2
    # Find And Remote Home
    # invariants:
    #   the bot's existence is always confirmed with minimum cost by remote to nearest neighbor

    print("Started Stage 2")

    for segment in segments[2:4]:
        for vertex in segment:
            neighbors = client.G.adj[vertex]
            nearest_neighbor = min(neighbors, key=lambda n: client.G.edges[vertex, n]['weight'])
            if client.remote(vertex, nearest_neighbor):
                counter += remote_path(client, shortest_path_to_home, nearest_neighbor)
                if counter == client.l:
                    score = client.end()
                    return score

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


def remote_path(client, shortest_paths, vertex):
    path = shortest_paths[vertex]
    path = path[::-1]
    action = 0
    for e in range(len(path) - 1):
        action = client.remote(path[e], path[e + 1])
    return action
