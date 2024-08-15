import random
from collections import Counter
import copy 

def randomize(l):
    final = []
    for _ in range(len(l)):
        if len(l)==1:
            final.append(l[0])
            return final
        idx = random.randint(0,len(l)-1)
        final.append(l[idx])
        l.remove(l[idx])
L = [random.randint(0,10) for _ in range(10)]
L_Copy = copy.deepcopy(L)
print(L_Copy)
L1 = randomize(L)
print(L1)
print(Counter(L1)==Counter(L_Copy))


class Rrand:
    def __init__(self, l):
        self.randomized = randomize(l)

R = Rrand([random.randint(0,100) for _ in range(20)])
print(R.randomized)

