import numpy as np

mass = [[0, 2, 0, 0, 3],
           [1, -1, 0, 8, 0],
           [-3, 3, 0, 0, 0],
           [-3, -1, 0, 0, 4],
           [0, -1, -8, 11, -2]]
b = np.zeros(5)
b = [50, 160, 0, 0, 0]
c = np.zeros(5)

# не успела расписать гаусса

print(np.linalg.solve(mass, b)) # ответ с использованием метода класса np

