import numpy as np
import plotly.graph_objects as go


def f(x):
    return np.cos(x) / (x + 2)


def integrate_simpson(a, b, eps):
    ans_y = []
    ans_x = []
    p = []
    n = 2
    ans_x.append(n)
    h = (b - a) / n
    integral_old = 0
    integral_new = (b - a) / 6 * (f(a) + 4 * f((a+b)/2) + f(b))
    print(f"h/{n} integral {integral_new}")
    ans_y.append(abs(integral_new - tochn))

    while abs(integral_new - integral_old) > eps:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = 0
        for i in range(0, n):
            x0 = x[i]
            x1 = x[i + 1]
            xm = (x1+x0) / 2.0
            integral_new += ((x1-x0) / 6) * (f(x0) + 4 * f(xm) + f(x1))
        print(f"h/{n} integral {integral_new}")
        print(f"e{n/2}/e{n} = {integral_old/integral_new}")
        print(f"integral1 - integral2 = {abs(integral_new - integral_old)} ")
        p.append(integral_old/integral_new)
    print(f"2^p = {sum(p)/len(p)}")
    pm = sum(p)/len(p)
    pt = np.log2(pm)
    print(pt)
    # integral_new = (h / 3) * (f(x[0]) + 2 * sum(f(x[2:-1:2])) + 4 * sum(f(x[1::2])) + f(x[-1]))
    # ans_y.append(abs(integral_new - tochn))
    # ans_x.append(n)

    return integral_new, n, ans_x, ans_y


def integrate_rectangle_left(a, b, eps, tochn, n=2):
    ans_x = []
    ans_y = []
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


a = 0.4
b = 1.2
eps = 1e-12
tochn = 0.19898816541819955



result1, n, x_sim, y_sim = integrate_simpson(a, b, eps)
# result2, x_l, y_l = integrate_rectangle_left(a, b, eps, tochn)
# result3, x_m, y_m = integrate_rectangle_mid(a, b, eps, tochn)
# result4, x_l1, y_l1 = integrate_rectangle_left(a, b, eps, tochn, 100)


data = [
    go.Scatter(x=x_sim, y=y_sim, mode='lines+markers', name='Simpson'),
    # go.Scatter(x=x_l, y=y_l, mode='lines+markers', name='Rectangle Left'),
    # go.Scatter(x=x_m, y=y_m, mode='lines+markers', name='Rectangle Mid'),
    # go.Scatter(x=x_l1, y=y_l1, mode='lines+markers', name='Rectangle Left')
]
fig = go.Figure(data=data)
fig.update_layout(
    xaxis_type="log", yaxis_type="log",
    xaxis_title="Количество разбиений n",
    yaxis_title="Ошибка"
)
fig.show()

print(f"Значение интеграла (Simpson): {result1}")
# print(f"Значение интеграла (Rectangle Left): {result2}")
# print(f"Значение интеграла (Rectangle Mid): {result3}")
