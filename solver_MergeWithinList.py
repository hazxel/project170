import networkx as nx
import random
from helper_functions import *

'''
To test locally, please do the following:

    Run the local server using "python local_server.py“ in terminal.

    This will start a web server that your client will now connect to. It will pick a random input instance to serve. An instance is a set of parameters (such as bot locations or student correctness) of the problem.

    In a separate terminal, run "python client.py --solver solver". The --solver flag indicates the solver python file the client should use. It's the file name of your solver, with .py omitted.

    If you want to try a different solver run "python client.py --solver <MY_SOLVER_NAME>"

    In both terminals, you should see a slew of scout and remote calls succeeding. At the bottom of the client terminal your score is shown. The score should be very low (since it's unlikely all bots were moved home).
'''


# average score: 90.97259925442

def solve(client):
    client.end()
    client.start()

    # print(shortestPathfromHome(client)[1][::-1])
    vote = votes(client)
    # print('The estimated accuracy of students is '+str(estimatedAccuracy(client, vote)))
    vote = np.array(vote)
    printVote(vote)
    ac = estimatedAccuracy(client, vote)
    print("Accuracy is: " + str(ac))
    seq = vote.argsort()
    seq = seq[::-1]
    seq = seq + 1
    count = 0

    Q = []  # vertices in Q must be checked anyway
    for i in range(client.l):
        Q.append(seq[0])
        seq = np.delete(seq, [0])
    while (count < client.l - 1):
        minW = 100000
        for i in range(1, len(Q)):
            if client.G.edges[Q[0], Q[i]]['weight'] < minW:
                minW = client.G.edges[Q[0], Q[i]]['weight']
                to = i
        knownBots = client.bot_count[Q[0]]
        frum = int(Q[0])
        to = int(Q[to])
        if client.G.edges[Q[0], client.h]['weight'] < minW:
            to = client.h
        # print("known bots: " + str(knownBots))
        count = count + client.remote(frum, to) - knownBots
        # print("Count is: " + str(count))
        del Q[0]
        if len(Q) < client.l - count:
            nextAcc = calCorrectProb(client, vote, ac, seq[0])
            if nextAcc < 0.6:
                break
            Q.append(seq[0])
            seq = np.delete(seq, [0])

    knownBots = client.bot_count[Q[0]]
    count = count + client.remote(int(Q[0]), client.h) - knownBots
    del Q[0]
    print("Now directly remote home:")
    print("Count is: " + str(count))

    costinSeq = []
    for v in Q:
        seq = np.append(v, seq)
    seq = seq.tolist()
    seq.remove(client.h)
    seq = np.array(seq)
    for v in seq:
        punishment = 1
        if calCorrectProb(client, vote, ac, v) < 0.2:
            punishment = 1.5
        if v != client.h:
            costinSeq.append(
                (1 - calCorrectProb(client, vote, ac, v)) * client.G.edges[v, client.h]['weight'] * punishment)

    costinSeq = np.array(costinSeq)
    newSeq = costinSeq.argsort()

    for i in newSeq:
        # print("count: " + str(count))
        if count == client.l:
            break
        knownBots = client.bot_count[int(seq[i])]
        count = count + client.remote(int(seq[i]), client.h) - knownBots
    # remoteKnownBotHome(client)

    score = client.end()
    print("The input was: V", client.v, " E: ", client.e, " L: ", client.l, " K: ", client.k)
    return score
