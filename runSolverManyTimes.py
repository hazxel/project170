from solver_FindAllandRemote import *
from ModifiedClient import *


N = 50
c = Client(False)
score = []
client.end()

for i in range(1， N + 1):
    print("Starting run #", i)
    s = solve(c)
    score.append(s)
    
    score_all = np.mean(score)
	score_top_87 = np.mean(np.sort(score)[::-1][:int(np.ceil(len(score) * 0.87))])

	print('		Have run ' + str(i) + ' tests, the average score is: ' + str(score_all))
	print('		Have run ' + str(i) + ' tests, the top 87%  score is: ' + str(score_top_87))
	print('----------run finished----------')
    print('')
