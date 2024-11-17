import numpy as np
#
#
# def f(x):
#     return np.exp(x)
#
#
# def fdx_approximation(x, h):
#     A, B, C = -1 / (2 * h), 0, 1 / (2 * h)
#
#     fdx = A * f(x - h) + B * f(x) + C * f(x + h)
#     return fdx
#
#
# x = 1
# h = 1e-5
#
# result = fdx_approximation(x, h)
# print(f" f'(x) = {result}")


def f(x):
    return np.exp(x)


def forward_difference(f, x, h):
    return (f(x + h) - f(x)) / h


def backward_difference(f, x, h):
    return (f(x) - f(x - h)) / h


def central_difference(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


x = 1

h = 1e-5

forward_diff = forward_difference(f, x, h)
backward_diff = backward_difference(f, x, h)
central_diff = central_difference(f, x, h)

exact_derivative = np.exp(x)

print(f"Производная методом разности вперед: {forward_diff}")
print(f"Производная методом разности назад: {backward_diff}")
print(f"Производная методом центральной разности: {central_diff}")
print(f"Точное значение производной: {exact_derivative}")
print(f"Погрешность разности вперед: {abs(forward_diff - exact_derivative)}")
print(f"Погрешность разности назад: {abs(backward_diff - exact_derivative)}")
print(f"Погрешность центральной разности: {abs(central_diff - exact_derivative)}")

