import numpy as np
import plotly.graph_objects as go

def f(x):
    return x - 200*np.tan(x)

def df(x):
    return 1 - 200*(1/(1-x**2))

def method_newton(x0, e=1e-15, chsi=0.7034395711636394):
    it = []
    yd = []
    x = x0
    i = 0
    ea = float('inf')  # Начальная погрешность
    while ea > e:
        i += 1
        it.append(i)
        x_old = x
        fx = f(x)
        yd.append(abs(x - chsi) / chsi)
        dfx = df(x)
        x = x - fx / dfx
        if x == 0:
            return x, i, it, yd
        ea = abs((x - x_old) / x)
    return x, i, it, yd


def mod_regula_falsi(xl, xu, es=10**-15, imax=10**16, chsi = 0.7034395711636394):
    yd = []
    it = []
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
        it.append(iter)
        yd.append(abs(xr-chsi)/chsi)
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

    return xr, iter, it, yd


a = 1
b = 2
x0 = 1
x1 = 2
ans = []
x_m, iterations, i_mrf, y_mrf = mod_regula_falsi(1, 2)
ans.append(x_m)
x_m, iterations, i_mrf, y_mrf = mod_regula_falsi(4, 5)
ans.append(x_m)
x_m, iterations, i_mrf, y_mrf = mod_regula_falsi(7, 8)
ans.append(x_m)
x_m, iterations, i_mrf, y_mrf = mod_regula_falsi(10, 11.6)
ans.append(x_m)
x_m, iterations, i_mrf, y_mrf = mod_regula_falsi(14, 15)
ans.append(x_m)
print(*ans)
n = 1000000
x = np.linspace(0, 15, n)
y = f(x)
data = [go.Scatter(x=x, y=y, name='func')]
fig = go.Figure(data=data)
fig.show()
fig.write_image('1.png', scale=1)
