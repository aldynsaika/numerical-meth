import plotly.graph_objects as go
import numpy as np
import math
import time


def f(x):
    return 4 * (1 - x**2) - np.exp(x)


def df(x):
    return -8 * x - np.exp(x)


def mod_regula_falsi(xl, xu, es=10**-15, imax=10**16):
    iter = 0
    xr = xl
    ea = float('inf')
    fl = f(xl)
    fu = f(xu)
    il = 0
    iu = 0

    while ea > es and iter < imax:
        xrold = xr
        xr = xu - (fu * (xl - xu)) / (fl - fu)
        fr = f(xr)
        iter += 1

        if xr != 0:
            ea = abs((xr - xrold) / xr)

        test = fl * fr

        if test < 0:
            xu = xr
            fu = f(xu)
            iu = 0
            il += 1
            if il >= 2:
                fl /= 2
        elif test > 0:
            xl = xr
            fl = f(xl)
            il = 0
            iu += 1
            if iu >= 2:
                fu /= 2
        else:
            ea = 0

    return xr, iter


def regula_falsi(a, b, e=10**-15):
    fa, fb = f(a), f(b)
    i = 0
    ea = float('inf')  # Начальная погрешность
    c = a
    while abs(b - a) > e and ea > e:
        i += 1
        c_old = c
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        ea = abs((c - c_old) / c)

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, i


def method_newton(x0, e=1e-15):
    x = x0
    i = 0
    ea = float('inf')  # Начальная погрешность
    while ea > e:
        i += 1
        x_old = x
        fx = f(x)
        dfx = df(x)
        x = x - fx / dfx
        ea = abs((x - x_old) / x)
    return x, i


def method_secant(x0, x1, e=1e-15):
    i = 0
    ea = float('inf')  # Начальная погрешность
    while ea > e:
        i += 1
        f0, f1 = f(x0), f(x1)
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        ea = abs((x2 - x1) / x2)
        x0, x1 = x1, x2
    return x1, i


def method_steff(x0, e=1e-15):
    x = x0
    i = 0
    ea = float('inf')  # Начальная погрешность
    while ea > e:
        i += 1
        x_old = x
        f0 = f(x)
        gx = f(x + f0)
        x1 = x - (f0**2) / (gx - f0)
        ea = abs((x1 - x_old) / x1)
        x = x1
    return x, i


# Начальные данные
a = 0
b = 1
x0 = 0.5
x1 = 0.8

# Измерение времени и выполнение методов
start = time.perf_counter()
x, iterations = regula_falsi(a, b)
end = time.perf_counter()
print(f"Метод regula falsi\nКорень: {x} Итерации: {iterations} Время: {end - start} секунд\n")

start = time.perf_counter()
x, iterations = mod_regula_falsi(a, b)
end = time.perf_counter()
print(f"Модифицированный метод regula falsi\nКорень: {x} Итерации: {iterations} Время: {end - start} секунд\n")

start = time.perf_counter()
x, iterations = method_newton(x0)
end = time.perf_counter()
print(f"Метод Ньютона\nКорень: {x} Итерации: {iterations} Время: {end - start} секунд\n")

start = time.perf_counter()
x, iterations = method_secant(x0, x1)
end = time.perf_counter()
print(f"Метод секущих\nКорень: {x} Итерации: {iterations} Время: {end - start} секунд\n")

start = time.perf_counter()
x, iterations = method_steff(x0)
end = time.perf_counter()
print(f"Метод Стеффенсена\nКорень: {x} Итерации: {iterations} Время: {end - start} секунд\n")


# Построение графика функции
# n = 10000
# x = np.linspace(-3, 3, n)
# y1 = f(x)
#
# data = [go.Scatter(x=x, y=y1, name='func')]
# fig = go.Figure(data=data)
# fig.show()
# fig.write_image('task2.png', scale=1)
