import matplotlib.pyplot as plt

x = [1,2,3,4,5,6]
y = [3,4,5,6,7,8]

plt.plot(x[1:], y[1:], 'ro')
plt.plot(x[0], y[0], 'g*')

plt.show()