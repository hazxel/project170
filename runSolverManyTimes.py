from solver_MergeWithinList import *
from ModifiedClient import *

N = 50
client = Client(False)
score = 0
client.end()

for i in range(1, N + 1):
    print("Starting run #", i)
    cur = solve(client)
    score += cur
    print("Average score: ", score / i)
    print('----------run finished----------')
    print('')

score /= N

print('Finished running ' + str(N) + ' tests, final average score is: ' + str(score))
