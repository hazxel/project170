from solver_MergeWithinList2 import *
from ModifiedClient import *
import numpy as np


N = 500
c = Client(False)
score = []
c.end()

for i in range(1, N + 1):
    s = solve(c)
    score.append(s)

    if score[i-1] < 82:
        raise Exception("bug is here!")
    
    score_all = np.mean(score)
    score_top_87 = np.mean(np.sort(score)[::-1][:int(np.ceil(len(score) * 0.87))])
    print('')
    print('------------run # {}------------'.format(i))
    print('The average score is: {}'.format(score_all))
    print('The top 87% score is: {}'.format(score_top_87))
    print('----------run finished----------')
    print('')
