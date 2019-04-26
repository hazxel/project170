
from solver_ScoutandRemote import*
from ModifiedClient import*

N = 10

c = Client(False)

score = 0

for i in range(N):
    score += solve(c)

score /= N

print('Have run ' + str(N) + ' tests, the average score is: ' + str(score))