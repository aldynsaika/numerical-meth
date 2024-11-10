import numpy as np
import plotly.graph_objects as go

def f(x):
    return np.cos(x) / (x + 2)

def integrate_simpson(a, b, eps, tochn):
    ans_y = []
    ans_x = []
    n = 2
    ans_x.append(n)
    h = (b - a) / n
    integral_old = 0
    integral_new = (h / 3) * (f(a) + 4 * f(a + h) + f(b))
    ans_y.append(abs(integral_new - tochn))

    while abs(integral_new - integral_old) > eps:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = (h / 3) * (f(x[0]) + 2 * sum(f(x[2:-1:2])) + 4 * sum(f(x[1::2])) + f(x[-1]))
        ans_y.append(abs(integral_new - tochn))
        ans_x.append(n)

    return integral_new, n, ans_x, ans_y

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
    integral_new = sum(f((x[:-1] + x[1:]) / 2)) * h  # Центр прямоугольников
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


a = 0.4
b = 1.2
eps = 1e-6
tochn = 0.19898816541819955

result1, n, x_sim, y_sim = integrate_simpson(a, b, eps, tochn)
result2, x_l, y_l = integrate_rectangle_left(a, b, eps, tochn)
result3, x_m, y_m = integrate_rectangle_mid(a, b, eps, tochn)


data = [
    go.Scatter(x=x_sim, y=y_sim, mode='lines+markers', name='Simpson'),
    go.Scatter(x=x_l, y=y_l, mode='lines+markers', name='Rectangle Left'),
    go.Scatter(x=x_m, y=y_m, mode='lines+markers', name='Rectangle Mid')
]
fig = go.Figure(data=data)
fig.update_layout(
    xaxis_type="log", yaxis_type="log",
    xaxis_title="Количество разбиений n",
    yaxis_title="Ошибка"
)
fig.show()

print(f"Значение интеграла (Simpson): {result1}")
print(f"Значение интеграла (Rectangle Left): {result2}")
print(f"Значение интеграла (Rectangle Mid): {result3}")
