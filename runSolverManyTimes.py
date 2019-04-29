from solver_FindAllandRemote import *
from ModifiedClient import *

N = 100
c = Client(False)
score = []

for i in range(N):
    print("Starting run #", i+1)
    s = solve(c)
    score.append(s)

score_all = np.mean(score)
score_top_87 = np.mean(np.sort(score)[::-1][:int(np.ceil(len(score) * 0.87))])

print('Have run ' + str(N) + ' tests, the average score is: ' + str(score_all))
print('Have run ' + str(N) + ' tests, the top 87%  score is: ' + str(score_top_87))
