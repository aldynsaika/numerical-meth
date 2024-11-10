import numpy as np


def f(x):
    return np.exp(x)


def fdx_approximation(x, h):
    A, B, C = -1 / (2 * h), 0, 1 / (2 * h)

    fdx = A * f(x - h) + B * f(x) + C * f(x + h)
    return fdx


x = 1
h = 1e-5

result = fdx_approximation(x, h)
print(f" f'(x) = {result}")
