import plotly.graph_objects as go
import numpy as np
import math
import time


def f(x):
    return 4 * (1 - x**2) - np.exp(x)


def method_steff(x0, e=1e-15, chsi = 0.7034395711636394):
    it = []
    yd = []
    y = []
    x = x0
    i = 0
    ea = float('inf')
    while ea > e:
        i += 1
        it.append(i)
        x_old = x
        f0 = f(x)
        yd.append(abs(x-chsi)/chsi)
        y.append(f0)
        gx = f(x + f0)
        x1 = x - (f0**2) / (gx - f0)
        ea = abs((x1 - x_old) / x1)
        x = x1
    return x, i, it, yd, y



