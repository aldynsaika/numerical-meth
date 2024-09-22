import plotly.graph_objects as go
import numpy as np
import math


def f(x):
    v = 40
    t = 10
    g = 9.8
    m = 68.1
    return (((g*m)/x) * (1 - math.exp(-(x/m)*t)) - v)


#модифицированный regula falsi
def mod_regula_falsi(xl, xu, es, imax):
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
    return xr, iter, ea

def dichotomy(a, b, e):
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError("Функция должна иметь разные знаки на концах интервала")

    while (b - a) / 2 > tol:
        c = (a + b) / 2
        fc = f(c)
        if fc == 0:
            return c
        elif fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
    return (a + b) / 2

#regula falsi
# def regula_falsi(b, a):
#     while b - a > e:
#         c = (b - a) / 2
#         if (func1(a) * func1(c)) > 0:
#             a = c
#         if (func1(a) * func1(c)) < 0:
#             b = c
#         if (func1(a) * func1(c)) == 0:
#             ans = c
#             break
#         ans = a
#     return ans


c = 0
a = 1
b = 100
e = 0.00001
ans = 0


# ans = regula_falsi(b, a)

x, iterations, error = mod_regula_falsi(a, b, e, 1000)
print(f"Модифицированный метод\nКорень: {x} Итерации:{iterations} Ошибка: {error}")




# n = 1000
# x = np.linspace(0, n, n)
# y1 = []
# for i in range(1, n+1):
#         curr = func1(c)
#         y1.append(curr)
#
# y1 = np.array(y1)[:n]
#
# data = [go.Scatter(x=x, y=y1, name='func')
#         ]
# fig = go.Figure(data=data)
# fig.show()
# fig.write_image('task2.png', scale = 1)
