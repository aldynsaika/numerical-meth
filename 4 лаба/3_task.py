import numpy as np

def f(x):
    return 1/(1+np.exp(x))

def integrate_simpson(a, b, eps):
    n = 2
    h = (b - a) / n
    integral_old = 0
    integral_new = h / 3 * (f(a) + 4 * f(a + h) + f(b))

    while abs(integral_new - integral_old) > eps:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = h / 3 * (f(x[0]) + 2 * sum(f(x[2:-1:2])) + 4 * sum(f(x[1::2])) + f(x[-1]))

    return integral_new


a = -5
b = 5
eps = 1e-15

result = integrate_simpson(a, b, eps)
print(f"Значение интеграла: {result}")
