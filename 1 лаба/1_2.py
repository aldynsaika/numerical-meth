import math

import plotly.graph_objects as go
import numpy as np
from datetime import datetime

e = 1.0

while (1+e/2 > 1):
    e = e/2

start_time1 = datetime.now() # включаем счетчик

n1 = 10**8
x = np.linspace(0, n1, n1)
y1 = [1]
y2 = np.log(2)
y3 = []
k = -1
curr = 0
delta1 = 0

y3.append((1-np.log(2))/np.log(2))

for i in range(1, n1):
        k = k*(-1)
        curr += k*(1/i)
        delta1 = abs(curr-np.log(2))/np.log(2)
        y1.append(curr)
        y3.append(delta1)

t1 = datetime.now() - start_time1
print(datetime.now() - start_time1)

start_time2 = datetime.now()

print(n1, delta1)

n2 = 1000
delta2 = 0
curr = 0

for i in range(1, n2):
        k = k*(-1)
        curr += k*(1/i)
        delta2 = abs(curr-np.log(2))/np.log(2)
        y1.append(curr)
        y3.append(delta1)

t2 = datetime.now() - start_time2

print(n2, delta2)
alfa = delta1-delta2/n1-n2
print(delta1-delta2/n1-n2)
beta = delta1 - (delta1-delta2/n1-n2)*n1
print(delta1 - (delta1-delta2/n1-n2)*n1)

n_e = (e - beta)/alfa
print(n_e)
print(n_e*2.5554444*10**-6)



data = [go.Scatter(x=x, y=y1, name='func'),
        go.Scatter(x=x, y=[y2]*n1, name='ln2'),
        go.Scatter(x=x, y=y3, name='delta')
        ]



fig = go.Figure(data=data)
fig.update_layout(xaxis_type="log", yaxis_type="log")
fig.show()
fig.write_image('task2.png', scale = 1)