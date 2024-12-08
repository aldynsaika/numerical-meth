import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 1 / (1 + np.exp(x))

def integrate_simpson(a, b, eps):
    ans_y = []
    ans_x = []
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

        ans_y.append(abs(integral_new - integral_old))  # Обновляем разницу
        ans_x.append(n)

    return integral_new, ans_x, ans_y


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
# Задаем параметры интегрирования
a = -5
b = 5
eps = 1e-15

# Выполняем интегрирование для всех методов
result_simpson, x_simpson, y_simpson = integrate_simpson(a, b, eps)
print(f"Значение интеграла (Simpson): {result_simpson}")

result_left_rectangle, x_left, y_left = integrate_rectangle_left(a, b, eps)
print(f"Значение интеграла (Left Rectangle): {result_left_rectangle}")

result_mid_rectangle, x_mid, y_mid = integrate_rectangle_mid(a, b, eps)
print(f"Значение интеграла (Mid Rectangle): {result_mid_rectangle}")

# Построение графиков зависимости ошибки от n
plt.figure(figsize=(12, 8))

plt.plot(x_simpson, y_simpson, label='Метод Симпсона', marker='o')
plt.plot(x_left, y_left, label='Левые прямоугольники', marker='o')
plt.plot(x_mid, y_mid, label='Средние прямоугольники', marker='o')

plt.yscale('log')  # Логарифмическая шкала для оси Y
plt.xscale('log')  # Логарифмическая шкала для оси X
plt.xlabel('Количество разбиений (n)')
plt.ylabel('Ошибка')
plt.title('Зависимость ошибки от количества разбиений (n)')
plt.legend()
plt.grid()
plt.show()
