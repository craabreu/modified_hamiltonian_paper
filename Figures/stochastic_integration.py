import itertools
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import figstyle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

n = [2, 6]
cases = [pd.read_csv(f'stochastic_n{i}.csv') for i in n]

N = len(cases)
fig, ax = plt.subplots(N, 1, figsize=(3.37,2*N), sharex=True)
fig.subplots_adjust(hspace=0.1)

methods = {}
# methods['euler_maruyama'] = 'Euler-Maruyama'
methods['strong_taylor'] = 'Order-1.5 Strong It\\={o}-Taylor Method'
methods['midpoint'] = 'Trapezoidal-Rule Approximation'
methods['stationary'] = 'Perturbed Ornstein-Uhlenbeck'
marker = ['o', 's', '^', 'v', '>', '<']

for i, case in enumerate(cases):
    ax[i].set_xscale('log')
    ax[i].set_yscale('log')
    ax[i].set_ylabel(f'$L^1$ Error (n={n[i]})')
    for j, (method, title) in enumerate(methods.items()):
        ax[i].plot(case['dt'], case[method], label=title, marker=marker[j])

ax[N-1].legend()
ax[N-1].set_xlabel('$\\gamma h$ (friction constant $\\times$ step size)')

# Plot histograms as inset:
inset = inset_axes(ax[0], width="100%", height="100%",
                    bbox_to_anchor=(.2, .5, .5, .5),
                    bbox_transform=ax[0].transAxes)

step_sizes = [1000, 10000]
histograms = [pd.read_csv(f'stationary/stationary_2_{dt}.hist') for dt in step_sizes]
vlim=math.sqrt(2)
colors = ['blue', 'orange']
for H, dt, color in zip(histograms, step_sizes, colors):
    # inset.bar(H['v'], H[' rho(v)'], width=math.sqrt(2)/len(H.index), label=f'$\\gamma h$ = {dt/10000}')
    x = H['v'].values.copy()
    y = H[' rho(v)'].values.copy()
    inset.plot(x, y, label=f'$\\gamma h$ = {dt/10000}', color=color)
    inset.plot([x[0], x[0], np.nan, x[-1], x[-1]], [0, y[0], np.nan, y[-1], 0], color=color, linestyle='--')
    inset.fill_between(H['v'], 0, H[' rho(v)'], color=color, alpha=0.2)
inset.set_xlabel('$\\hat{v}$')
inset.set_ylabel('$\\rho(\\hat{v})$')
inset.set_ylim(bottom=0)
# inset.set_ylim([0, 0.015])
inset.xaxis.set_ticklabels([])
inset.yaxis.set_ticklabels([])
inset.legend(loc='lower center')


fig.savefig('stochastic_integration')
plt.show()
