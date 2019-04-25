import math
import numpy as np
import matplotlib.pyplot as plt
import figstyle
from scipy.special import gamma

cases = [1, 2, 3, 6]
colors = ['r', 'g', 'b', 'm']

def plot_H_contribution(index, x):
    ax[index].set_ylabel('$\\mathcal{H}$ contribution ($kT$)')
    for n, color in zip(cases, colors):
        ax[index].plot(x, n*np.log(np.cosh(x/math.sqrt(n))), f'{color}-', label=f'$n={n}$')
    ax[index].plot(x, x**2/2, 'k-', label='original')
    ax[index].set_ylim([0, 2])
    ax[index].legend()

def plot_velocity(index, x):
    ax[index].set_ylabel('Reduced Velocity $\\left(\\hat{v}_i = \\frac{v_i}{\\sqrt{kT/m_i}}\\right)$')
    # ax[index].set_ylabel('Velocity $\\left(\\sqrt{\\frac{m_i}{kT}} v_i\\right)$')
    for n, color in zip(cases, colors):
        ax[index].plot(x, math.sqrt(n)*np.tanh(x/math.sqrt(n)), f'{color}-', label=f'$n={n}$')
    ax[index].plot(x, x, 'k-', label='original')
    ax[index].set_ylim([-3, 3])
    ax[index].legend()

def factor(n):
    return gamma((n+1)/2)/(gamma(n/2)*np.sqrt(math.pi*n))

def plot_momentum_distribution(index, x):
    def density(n):
        return lambda x: factor(n)/np.cosh(x/np.sqrt(n))**n
    ax[index].set_ylabel('Probability Density')
    alpha = 0.1
    for n, color in zip(cases, colors):
        ax[index].plot(x, density(n)(x), f'{color}-', label=f'$n={n}$')
        ax[index].fill_between(x, 0, density(n)(x), color=color, alpha=alpha)
    ax[index].plot(x, np.exp(-x**2/2)/np.sqrt(2*math.pi), 'k-', label='original')
    ax[index].fill_between(x, 0, np.exp(-x**2/2)/np.sqrt(2*math.pi), color='k', alpha=alpha)
    ax[index].set_ylim([0, 0.42])
    ax[index].legend()

def plot_velocity_distribution(index, xinp):
    def density(n):
        return lambda x: factor(n)*(1 - x**2/n)**(n/2 - 1)
    ax[index].set_ylabel('Probability Density')
    alpha = 0.1
    for n, color in zip(cases, colors):
        sqrtn = np.sqrt(n)
        x = xinp[xinp**2 < n]
        y = density(n)(x)
        if n < 3:
            ax[index].plot([-sqrtn, -sqrtn, np.nan, sqrtn, sqrtn], [0, y[0], np.nan, y[-1], 0], f'{color}--')
            x = np.append(np.insert(x, 0, [-sqrtn, np.nan, -sqrtn]), [sqrtn, np.nan, sqrtn])
            y = np.append(np.insert(y, 0, [0, np.nan, y[0]]), [y[-1], np.nan, 0])
        prepend = xinp[xinp < -sqrtn]
        append = xinp[xinp > sqrtn]
        x = np.append(np.insert(x, 0, prepend), append)
        y = np.append(np.insert(y, 0, np.zeros_like(prepend)), np.zeros_like(append))
        ax[index].plot(x, y, f'{color}-', label=f'$n={n}$')
        ax[index].fill_between(x, 0, y, color=color, alpha=alpha)
    ax[index].plot(xinp, np.exp(-xinp**2/2)/np.sqrt(2*math.pi), 'k-', label='original')
    ax[index].fill_between(xinp, 0, np.exp(-xinp**2/2)/np.sqrt(2*math.pi), color='k', alpha=alpha)
    ax[index].set_ylim([0, 0.8])
    ax[index].legend()


fig, ax = plt.subplots(2, 1, figsize=(3.4, 4), sharex=True)

limit = 4
# ax[0].set_xlabel('Momentum $\\left(\\frac{p_i}{\\sqrt{m_i k T}}\\right)$')
ax[0].set_xlim([-limit, limit])
x = np.linspace(-limit, limit, 200)
plot_momentum_distribution(0, x)

limit = 4
ax[1].set_xlabel('Reduced Momentum $\\left(\\hat{p}_i = \\frac{p_i}{\\sqrt{m_i k T}}\\right)$')
ax[1].set_xlim([-limit, limit])
x = np.linspace(-limit, limit, 200)
plot_velocity(1, x)
fig.savefig('momentum_functions')

fig, ax = plt.subplots(1, 1, figsize=(3.4, 2))
ax = [ax]

limit = 3
ax[0].set_xlabel('Reduced Velocity $\\left(\\hat{v}_i = \\frac{v_i}{\\sqrt{kT/m_i}}\\right)$')
ax[0].set_xlim([-limit, limit])
x = np.linspace(-limit, limit, 400)
plot_velocity_distribution(0, x)
fig.savefig('velocity_distributions')

plt.show()
