import plotly.graph_objects as go
import numpy as np
import math


def f(x):
    return 4*(1-x**2) - math.exp(x)


def df(x):
    return -8*x - np.exp(x)


def mod_regula_falsi(xl, xu, es=10**-15, imax=10**16):
    iter = 0
    xr = xl
    ea = 0
    fl = f(xl)
    fu = f(xu)
    il = 0
    iu = 0

    while True:
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

        if ea < es or iter >= imax:
            break
    return xr, iter


def regula_falsi(a, b, e=10**-15):
    fa, fb = f(a), f(b)
    i = 0
    while abs(b - a) > e:
        i += 1
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        if abs(fc) < e:
            return c, i
        elif fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, i


def method_newton(x0, e=1e-15):
    x = x0
    i = 0
    fx = 1
    while abs(fx) > e:
        i += 1
        fx = f(x)
        dfx = df(x)
        if fx == e:
            return x, i
        x = x - fx / dfx
    return x, i


def method_secant(x0, x1, e=1e-15):
    f1 = f(x1)
    i = 0
    while abs(f1) > e:
        i += 1
        f0, f1 = f(x0), f(x1)
        if abs(f1) == 0:
            return x1, i
        x2 = x1 - f1 * ((x1 - x0) / (f1 - f0))
        x0, x1 = x1, x2
    return x1, i


def method_steff(x0, e=1e-15):
    x = x0
    f0 = f(x)
    i = 0
    while abs(f0) > e:
        i += 1
        if abs(f0) == 0:
            return x, i
        gx = f(x + f0)
        x1 = x - ((f0**2) / (gx - f0))
        x = x1
        f0 = f(x)
    return x, i


a = 0
b = 1
x0 = 0.5
x1 = 0.8

x, iterations = regula_falsi(a, b)
print(f"Метод regula falsi\nКорень: {x} Итерации:{iterations}\n")

x, iterations = mod_regula_falsi(a, b)
print(f"Модифицированный метод regula falsi\nКорень: {x} Итерации:{iterations}\n")

x, iterations = method_newton(x0)
print(f"Метод Ньютона\nКорень: {x} Итерации:{iterations}\n")

x, iterations = method_secant(x0, x1)
print(f"Метод секущих\nКорень: {x} Итерации:{iterations}\n")

x, iterations = method_steff(x0)
print(f"Метод Стеффенсена\nКорень: {x} Итерации:{iterations}\n")

n = 10000
x = np.linspace(-3, 3, n)
y1 = f(x)


data = [go.Scatter(x=x, y=y1, name='func')
        ]
fig = go.Figure(data=data)
fig.show()
fig.write_image('task2.png', scale = 1)

