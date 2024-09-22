import plotly.graph_objects as go
import numpy as np
import math


def f(x):
    v = 40
    t = 10
    g = 9.8
    m = 68.1
    return (((g*m)/x) * (1 - math.exp(-(x/m)*t)) - v)


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


def dichotomy(a, b, e=10**-15):
    fa, fb = f(a), f(b)
    i = 0
    while (b - a) / 2 > e:
        i += 1
        c = (a + b) / 2
        fc = f(c)
        if fc == 0:
            return c, i
        elif fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
    return (a + b) / 2, i


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


c = 0
a = 10**-9
b = 200
ans = 0

x, iterations = dichotomy(a, b)
print(f"Метод дихотомии\nКорень: {x} Итерации:{iterations}\n")

x, iterations = regula_falsi(a, b)
print(f"Метод regula falsi\nКорень: {x} Итерации:{iterations}\n")

x, iterations = mod_regula_falsi(a, b)
print(f"Модифицированный метод regula falsi\nКорень: {x} Итерации:{iterations}")





n = 1000
x = np.linspace(0, n, n)
y1 = []
for i in range(1, n+1):
        curr = f(i)
        y1.append(curr)

y1 = np.array(y1)[:n]

data = [go.Scatter(x=x, y=y1, name='func')
        ]
fig = go.Figure(data=data)
fig.show()
fig.write_image('task2.png', scale = 1)
