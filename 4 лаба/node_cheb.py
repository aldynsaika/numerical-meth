import numpy as np


a, b = 0.4, 1.2

n = 10

chebyshev_nodes = np.cos(((2 * np.arange(1, n + 1) + 1) / (2 * n))* np.pi)
chebyshev_nodes = 0.5 * (a + b) + 0.5 * (b - a) * chebyshev_nodes

h_values = np.diff(chebyshev_nodes)
average_h = np.mean(h_values)

print("Узлы Чебышева:", chebyshev_nodes)
print("Шаги между узлами:", abs(h_values))
print("Средний оптимальный шаг h:", abs(average_h))
