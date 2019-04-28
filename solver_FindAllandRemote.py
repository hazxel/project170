import networkx as nx
import random
from helper_functions import*

'''
To test locally, please do the following:

    Run the local server using "python local_server.py“ in terminal.

    This will start a web server that your client will now connect to. It will pick a random input instance to serve. An instance is a set of parameters (such as bot locations or student correctness) of the problem.

    In a separate terminal, run "python client.py --solver solver". The --solver flag indicates the solver python file the client should use. It's the file name of your solver, with .py omitted.

    If you want to try a different solver run "python client.py --solver <MY_SOLVER_NAME>"

    In both terminals, you should see a slew of scout and remote calls succeeding. At the bottom of the client terminal your score is shown. The score should be very low (since it's unlikely all bots were moved home).
'''

def solve(client):
    client.end()
    client.start()
    
    # print(shortestPathfromHome(client)[1][::-1])

    findAllBots(client)

    # remoteKnownBotHome(client)
    
    score = client.end()
    print("The input was: V", client.v ," E: ", client.e, " L: ", client.l, " K: ", client.k)
    return score