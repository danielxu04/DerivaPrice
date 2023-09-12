import numpy as np
from numpy.random import normal
import matplotlib.pyplot as plt

def generate_ou_process(dt=0.1, mean_reversion_rate=1.2, mean=0.9, std=0.9, n=10000):
    # x(t=0) = 0
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = x[t-1] + mean_reversion_rate * (mean - x[t-1]) * dt + std * normal(0, np.sqrt(dt))
    return x

def plot_ou_process(x):
    plt.plot(x)
    plt.xlabel('t')
    plt.ylabel('x(t)')
    plt.title('Ornstein-Uhlenbeck Process')
    plt.show()