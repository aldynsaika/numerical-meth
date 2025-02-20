import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def f(x, y, lambda_):
    return lambda_*y


def exact_solution(x, lambda_):
    return np.exp(lambda_*x)


def euler_method(lambda_, h, x_end):
    x = np.arange(0, x_end + h, h)
    y = np.zeros_like(x)
    y[0] = 1

    for i in range(0, len(x)-1):
        y[i + 1] = y[i] + h * f(x[i], y[i], lambda_)
        #y[i+1] = y[i] + h * lambda_ * y[i]

    return x, y


def implicit_euler_method(lambda_, h, x_end):
    x = np.arange(0, x_end + h, h)
    y = np.zeros_like(x)
    y[0] = 1

    for i in range(0, len(x)-1):
        y[i+1] = y[i] * ((1+lambda_*(h/2))/(1-lambda_*(h/2)))

    return x, y


def improved_euler_method(lambda_, h, x_end):
    x = np.arange(0, x_end + h, h)
    y = np.zeros_like(x)
    y[0] = 1

    for i in range(0, len(x)-1):
        y_pred = y[i] + h * f(x[i], y[i], lambda_)
        y[i + 1] = y[i] + (h / 2) * (f(x[i], y[i], lambda_) + f(x[i+1], y_pred, lambda_))
        #y[i+1] = y[i] * (1 + h*lambda_ + ((lambda_*h)**2)/2)

    return x, y


def central_difference_method(lambda_, h, x_end):
    x = np.arange(0, x_end + h, h)
    y = np.zeros_like(x)
    y[0] = 1
    y_pred = y[0] + h * f(x[0], y[0], lambda_)
    y[1] = y[0] + (h / 2) * (f(x[0], y[0], lambda_) + f(x[0], y_pred, lambda_))

    for i in range(1, len(x)-1):
        y[i+1] = y[i-1] + 2*h*f(x[i], y[i], lambda_)

    return x, y


def error_analysis(method, lambda_, h_start, num_steps, x_end):
    errors = []
    h_values = [h_start / (2 ** i) for i in range(num_steps)]
    for h in h_values:
        x, y = method(lambda_, h, x_end)
        y_exact = exact_solution(x, lambda_)
        error = np.max(np.abs(y - y_exact))
        errors.append(error)

    p_values = np.zeros(len(h_values))

    for i in range(1, len(h_values)):
        p_values[i] = np.log2(errors[i - 1] / errors[i])
    return pd.DataFrame({"h": h_values, "error": errors, "p": p_values})


def plot_error(method, method_name, lambda_, h_start, num_steps, x_end):
    df = error_analysis(method, lambda_, h_start, num_steps, x_end)
    plt.loglog(df["h"], df["error"], marker='o', label=method_name)
    plt.xlabel("Шаг h")
    plt.ylabel("Ошибка")
    plt.title(f"Зависимость ошибки от шага (lambda = {lambda_})")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)


def main():
    h_start = 0.1
    num_steps = 10
    lambda_values = [-1, -5, -10, -15, -20, -25]
    x_end = 1

    for lambda_ in lambda_values:
        print(f"\nLambda = {lambda_}")
        print("\nМетод Эйлера:")
        print(error_analysis(euler_method, lambda_, h_start, num_steps, x_end))
        print("\nНеявный метод Эйлера:")
        print(error_analysis(implicit_euler_method, lambda_, h_start, num_steps, x_end))
        print("\nМетод Эйлера с пересчетом:")
        print(error_analysis(improved_euler_method, lambda_, h_start, num_steps, x_end))
        print("\nМетод центральных разностей:")
        print(error_analysis(central_difference_method, lambda_, h_start, num_steps, x_end))

    for lambda_ in lambda_values:
        plt.figure(figsize=(8, 6))
        plot_error(euler_method, "Метод Эйлера", lambda_, h_start, num_steps, x_end)
        plot_error(implicit_euler_method, "Неявный метод Эйлера", lambda_, h_start, num_steps, x_end)
        plot_error(improved_euler_method, "Метод Эйлера с пересчетом", lambda_, h_start, num_steps, x_end)
        plot_error(central_difference_method, "Метод центральных разностей", lambda_, h_start, num_steps, x_end)
        plt.show()


if __name__ == "__main__":
    main()

