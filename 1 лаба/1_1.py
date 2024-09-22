e = 1.0
max_n = 1.0
min_n = 1.0
count_max = 0
count_min = 0
count_zero = 0

# нахождение машинного нуля
while ( 1+e/2 > 1):
    e = e/2
    count_zero += 1

#нахождение максимального е
while (max_n*2 != float('inf')):
    max_n = max_n * 2
    count_max += 1
    # print(max_n, count_max)

# нахождение минимального е
while (min_n /2 > 0):
    min_n = min_n/2
    count_min += 1
    # print(min_n, count_min)

print(f"машинный ноль = {e}, степень двойки (с учетом скрытого бита) = {count_zero + 1}")
print(f"максимальное число {max_n} максимальная экспонента = {count_max}")
print(f"минимальное число {min_n} степень двойки (с учетом субнормальных чисел) = {count_min}, минимальная экспонента"
      f" = -{count_min - count_zero - 1}")
print(f"1, 1+e/2 = {1+e/2}, 1+e = {1+e}, 1 + e + e/2 = {1+e+e/2}")
print(f"1+10**(-16) + 10**(-16) = {1+10**(-16) + 10**(-16)}")
print(f"1+(10**(-16) + 10**(-16)) = {1+(10**(-16) + 10**(-16))}")

