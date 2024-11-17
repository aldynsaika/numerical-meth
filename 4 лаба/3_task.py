import numpy as np


def f(x):
    return 1/(1+np.exp(x))


def integrate_runge(a, b, eps):
    n = 1
    h = (b - a) / n
    integral_old = 0
    integral_new = sum(f(a + i * h) for i in range(n)) * h

    while True:
        n *= 2
        h = (b - a) / n
        integral_old = integral_new
        x = np.linspace(a, b, n + 1)
        integral_new = sum(f((x[:-1] + x[1:]) / 2)) * h  # метод средних прямоугольников

        if abs(integral_new - integral_old) / 3 < eps:
            break
    return integral_new


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


def integrate_rectangle_left(a, b, eps, tochn):
    ans_x = []
    ans_y = []
    n = 2
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    integral_new = 0
    integral_old = 0
    integral_new = sum(f(x[:-1])) * h
    ans_x.append(n)
    ans_y.append(abs(integral_new - tochn))

    while abs(integral_new - integral_old) > eps:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = sum(f(x[:-1])) * h
        ans_x.append(n)
        ans_y.append(abs(integral_new - tochn))

    return integral_new, ans_x, ans_y


def integrate_rectangle_mid(a, b, eps, tochn):
    ans_x = []
    ans_y = []
    n = 2
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    integral_new = 0
    integral_old = 0
    integral_new = sum(f((x[:-1] + x[1:]) / 2)) * h
    ans_y.append(abs(integral_new - tochn))
    ans_x.append(n)

    while abs(integral_new - integral_old) > eps:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = sum(f((x[:-1] + x[1:]) / 2)) * h
        ans_y.append(abs(integral_new - tochn))
        ans_x.append(n)

    return integral_new, ans_x, ans_y


a = -5
b = 5
eps = 1e-15

result = integrate_simpson(a, b, eps)
print(f"Значение интеграла: {result}")
