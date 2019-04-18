import networkx as nx
import random

'''
To test locally, please do the following:

    Run the local server using "python local_server.py in terminal".

    This will start a web server that your client will now connect to. It will pick a random input instance to serve. An instance is a set of parameters (such as bot locations or student correctness) of the problem.

    In a separate terminal, run "python client.py --solver solver". The --solver flag indicates the solver python file the client should use. It's the file name of your solver, with .py omitted.

    In both terminals, you should see a slew of scout and remote calls succeeding. At the bottom of the client terminal your score is shown. The score should be very low (since it's unlikely all bots were moved home).
'''

def solve(client):
    client.end()
    client.start()
    print("The Rescue begins:")
    print("    Home vertex: ", client.h)
    print("    Number of students: ", client.k)
    print("    Number of bots: ", client.l)
    print("    Number of vertices: ", client.v)
    print("    Number of edges: ", client.e)

    '''
    print("All the edges are:")
    for (u, v, wt) in client.G.edges.data('weight'):
        print('(%d, %d, %.3f)' % (u, v, wt))
    '''

    print("\n    Students' estimation of bot's existance of every vertex:\n    ", 
        votes(client))

    client.end()


### Returns a list which shows the number of students who believe there exists a bot on a certain vertex.
### Note that this function runs client.scout k*v times!!!
def votes(client):
    p = []
    vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    students = list(range(1, client.students + 1))
    for i in range(client.k):
        dict = client.scout(vertices[i], students)
        sum = 0
        for std in students:
            if dict[std] == True:
                sum = sum + 1
        p.append(sum)
    return p