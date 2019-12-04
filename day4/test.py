import numpy as np


passwords_1 = { i for i in range(271973, 785961 + 1)
                if (list(str(i)) == sorted(str(i))
                    and np.any(np.bincount(list(map(int, list(str(i))))) >= 2) == True) }

passwords_2 = { i for i in range(271973, 785961 + 1)
                if (list(str(i)) == sorted(str(i))
                    and np.any(np.bincount(list(map(int, list(str(i))))) == 2) == True) }

print(len(passwords_1)) # part one
print(len(passwords_2)) # part two