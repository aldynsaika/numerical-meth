import plotly.graph_objects as go
import numpy as np
import time


def f(x):
    v = 40
    t = 10
    g = 9.8
    m = 68.1
    return (((g * m) / x) * (1 - np.exp(-(x / m) * t)) - v)


def show_method(x, y, name):
    data = [go.Scatter(x=x, y=y, name=name, mode='lines+markers')]
    fig = go.Figure(data=data)
    fig.show()
    fig.write_image(f'{name}.png', scale=1)


def dichotomy(a, b, e=10 ** -15, chsi = 14.780203831661055):
    start_time = time.perf_counter()
    yd = []
    iterations = []
    fa, fb = f(a), f(b)
    i = 0
    while (b - a) / 2 > e:
        i += 1
        c = (a + b) / 2
        fc = f(c)
        iterations.append(i)
        yd.append(abs(c-chsi)/chsi)
        if fc == 0:
            print(f"time dichotomy {time.perf_counter() - start_time} seconds")
            return c, i, iterations, yd
        elif fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
    print(f"time dichotomy {time.perf_counter() - start_time} seconds")
    return (a + b) / 2, i, iterations, yd


def regula_falsi(a, b, e=10 ** -15, chsi = 14.780203831661055):
    start_time = time.perf_counter()
    yd = []
    iterations = []
    fa, fb = f(a), f(b)
    i = 0
    while abs(b - a) > e:
        i += 1
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        iterations.append(i)
        yd.append(abs(c-chsi)/chsi)
        if abs(fc) < e:
            print(f"time regula_falsi {time.perf_counter() - start_time} seconds")
            return c, i, iterations, yd
        elif fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    print(f"time regula_falsi {time.perf_counter() - start_time} seconds")
    return c, i, iterations, yd


def mod_regula_falsi(xl, xu, es=10 ** -15, imax=10 ** 16, chsi = 14.780203831661055):
    start_time = time.perf_counter()
    x = []
    y = []
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
        x.append(iter + 1)
        y.append(abs(xr-chsi)/chsi)
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
    print(f"time modified regula_falsi {time.perf_counter() - start_time} seconds")
    return xr, iter, x, y


# Начальные значения
a = 10 ** -9
b = 200


# Метод дихотомии
x, iterations, iter_list_dich, func_values_dich = dichotomy(a, b)
print(f"Метод дихотомии\nКорень: {x} Итерации:{iterations}\n")
# show_method(iter_list, func_values, 'Dichotomy Method')

# Метод regula falsi
x, iterations, iter_list_rf, func_values_rf = regula_falsi(a, b)
print(f"Метод regula falsi\nКорень: {x} Итерации:{iterations}\n")
# show_method(iter_list, func_values, 'Regula Falsi Method')

# Модифицированный метод regula falsi
x, iterations, iter_list_mrf, func_values_mrf = mod_regula_falsi(a, b)
print(f"Модифицированный метод regula falsi\nКорень: {x} Итерации:{iterations}\n")
# show_method(iter_list, func_values, 'Modified Regula Falsi Method')

data = [go.Scatter(x=iter_list_dich, y=func_values_dich, name='dichotomy'),
        go.Scatter(x=iter_list_rf, y=func_values_rf, name='regula falsi'),
        go.Scatter(x=iter_list_mrf, y=func_values_mrf, name='mod regula falsi')]
fig = go.Figure(data=data)
fig.update_layout(xaxis_type="log", yaxis_type="log")
fig.show()
fig.write_image(f'1.png', scale=1)

