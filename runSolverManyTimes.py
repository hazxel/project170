from solver_DistributionSegment import *
from ModifiedClient import *

N = 5
c = Client(False)
score = 0

for i in range(N):
    print("Starting run #", i+1)
    s = solve(c)
    score += s

score /= N

print('Have run ' + str(N) + ' tests, the average score is: ' + str(score))
