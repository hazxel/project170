from solver_FindAllandRemote import *
from ModifiedClient import *

N = 100
c = Client(False)
score = 0

for i in range(N):
    print("Starting run #", i+1)
    s = solve(c)
    score += s

score /= N

print('Have run ' + str(N) + ' tests, the average score is: ' + str(score))
