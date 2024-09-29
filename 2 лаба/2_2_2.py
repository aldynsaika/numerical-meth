import plotly.graph_objects as go
import numpy as np

def f(x):
    return (x**2) * np.exp(x)

def df(x):
    return (2*x + x**2) * np.exp(x)

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

def modified_method_newton(x0, m=2, e=1e-15):
    x = x0
    i = 0
    ea = float('inf')  # Начальная погрешность
    while ea > e:
        i += 1
        x_old = x
        fx = f(x)
        dfx = df(x)
        x = x - (m *(fx / dfx))
        ea = abs((x - x_old) / x)
    return x, i

x0 = 1e-6

x, iterations = method_newton(x0)
print(f"Метод Ньютона\nКорень: {x} Итерации: {iterations}\n")

x, iterations = modified_method_newton(x0)
print(f"Уточненный метод Ньютона\nКорень: {x} Итерации: {iterations}\n")




n = 10000
x = np.linspace(-3, 3, n)
y1 = f(x)

data = [go.Scatter(x=x, y=y1, name='func'),

        ]
fig = go.Figure(data=data)
fig.show()
fig.write_image('task2.png', scale = 1)
