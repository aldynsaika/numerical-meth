import numpy as np
import plotly.graph_objects as go


def f(x):
    return np.cos(x) / (x + 2)


def integrate_simpson(a, b, eps):
    ans_y = []
    ans_x = []
    p_values = []
    n = 2
    ans_x.append(n)

    # Первоначальное приближение
    h = (b - a) / n
    integral_old = 0
    integral_new = (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))

    ans_y.append(abs(integral_new - integral_old))  # Добавляем текущую разницу

    while abs(integral_new - integral_old) > eps:
        integral_old = integral_new  # Сохраняем старое значение
        n *= 2  # Увеличиваем число сегментов
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = 0

        # Расчет интеграла методом Симпсона для нового разбиения
        for i in range(0, n):
            x0 = x[i]
            x1 = x[i + 1]
            xm = (x1 + x0) / 2.0
            integral_new += ((x1 - x0) / 6) * (f(x0) + 4 * f(xm) + f(x1))

        # Оценка степени точности
        if len(ans_y) > 1:
            e_n = abs(integral_new - integral_old)  # Текущая ошибка
            e_prev = ans_y[-1]  # Предыдущая ошибка
            if e_n > 0:  # Избегаем деления на ноль
                p = np.log2(e_prev / e_n)
                p_values.append(p)

        ans_y.append(abs(integral_new - integral_old))  # Обновляем разницу
        ans_x.append(n)

    # Средняя степень точности
    average_p = sum(p_values) / len(p_values) if p_values else 0
    print(f"Средняя степень точности (Simpson): {average_p}")

    return integral_new, n, ans_x, ans_y


def integrate_rectangle_left(a, b, eps, n=2):
    ans_x = []
    ans_y = []
    p_values = []

    iteration_count = 0  # Счётчик итераций

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    integral_new = sum(f(x[:-1])) * h
    ans_x.append(n)
    ans_y.append(abs(integral_new))  # Первая ошибка

    print(f"Начальное значение (Left Rectangle): n={n}, integral={integral_new}")

    while True:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = sum(f(x[:-1])) * h

        error_new = abs(integral_new - integral_old)

        # Проверка на сходимость
        if error_new <= eps:  # Условие сходимости
            break

        if iteration_count >= 10:  # Предотвращение бесконечного цикла
            print("Превышено максимальное количество итераций.")
            break

        # Оценка степени точности
        if len(ans_y) > 0:
            e_prev = ans_y[-1]
            if error_new > 0:  # Избегаем деления на ноль
                p = np.log2(e_prev / error_new)
                p_values.append(p)

        ans_x.append(n)
        ans_y.append(error_new)

        iteration_count += 1

        # Вывод степени точности после первых 4 итераций
        if iteration_count == 4:
            if len(p_values) >= 2:  # Проверяем, что есть минимум 2 значения
                print(f"Степень точности после 4 итераций (Left Rectangle): p1={p_values[-2]}, p2={p_values[-1]}")

    return integral_new, ans_x, ans_y


def integrate_rectangle_mid(a, b, eps, n=2):
    ans_x = []
    ans_y = []
    p_values = []

    iteration_count = 0  # Счётчик итераций

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    integral_new = sum(f((x[:-1] + x[1:]) / 2)) * h
    ans_x.append(n)
    ans_y.append(abs(integral_new))  # Первая ошибка

    print(f"Начальное значение (Mid Rectangle): n={n}, integral={integral_new}")

    while True:
        integral_old = integral_new
        n *= 2
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        integral_new = sum(f((x[:-1] + x[1:]) / 2)) * h

        error_new = abs(integral_new - integral_old)

        # Проверка на сходимость
        if error_new <= eps:  # Условие сходимости
            break

        if iteration_count >= 10:  # Предотвращение бесконечного цикла
            print("Превышено максимальное количество итераций.")
            break

        # Оценка степени точности
        if len(ans_y) > 0:
            e_prev = ans_y[-1]
            if error_new > 0:  # Избегаем деления на ноль
                p = np.log2(e_prev / error_new)
                p_values.append(p)

        ans_x.append(n)
        ans_y.append(error_new)

        iteration_count += 1

        # Вывод степени точности после первых 4 итераций
        if iteration_count == 4:
            if len(p_values) >= 2:  # Проверяем, что есть минимум 2 значения
                print(f"Степень точности после 4 итераций (Mid Rectangle): p1={p_values[-2]}, p2={p_values[-1]}")

    return integral_new, ans_x, ans_y


# Параметры интегрирования
a = 0.4
b = 1.2
eps = 1e-12

# Выполнение интегрирования
result1, n_sim, x_sim, y_sim = integrate_simpson(a, b, eps)
result2, x_l, y_l = integrate_rectangle_left(a, b, eps)
result3, x_m, y_m = integrate_rectangle_mid(a, b, eps)

# Визуализация
data = [
    go.Scatter(x=x_sim, y=y_sim, mode='lines+markers', name='Simpson'),
    go.Scatter(x=x_l, y=y_l, mode='lines+markers', name='Rectangle Left'),
    go.Scatter(x=x_m, y=y_m, mode='lines+markers', name='Rectangle Mid'),
]

fig = go.Figure(data=data)
fig.update_layout(
    xaxis_type="log", yaxis_type="log",
    xaxis_title="Количество разбиений n",
    yaxis_title="Ошибка"
)
fig.show()

# Вывод результатов интегрирования
print(f"Значение интеграла (Simpson): {result1}")
print(f"Значение интеграла (Rectangle Left): {result2}")
print(f"Значение интеграла (Rectangle Mid): {result3}")
