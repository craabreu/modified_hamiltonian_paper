import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import glob
import figstyle
# import itertools
# marker = itertools.cycle(('s', '+', '^', '.', 'o', '*'))

method_and_n = [
    ('nhc_xi_respa', 0),
    ('baoab_respa', 0),
    ('stochastic_isokinetic_nhc_middle_respa', 1),
    ('stochastic_subkinetic_nhc_middle_respa', 1),
    # ('subkinetic_nhc_middle_respa', 1),
    # ('subkinetic_nhc_xi_respa', 1),
    ('trapezoidal_baoab_respa', 1),
    ('perturbed_OU_baoab_respa', 1),
    ('stochastic_isokinetic_nhc_middle_respa', 2),
    ('stochastic_subkinetic_nhc_middle_respa', 2),
    # ('subkinetic_nhc_middle_respa', 2),
    # ('subkinetic_nhc_xi_respa', 2),
    ('trapezoidal_baoab_respa', 2),
    ('perturbed_OU_baoab_respa', 2),
    ('stochastic_isokinetic_nhc_middle_respa', 4),
    ('stochastic_subkinetic_nhc_middle_respa', 4),
    # ('subkinetic_nhc_middle_respa', 4),
    # ('subkinetic_nhc_xi_respa', 4),
    ('trapezoidal_baoab_respa', 4),
    ('perturbed_OU_baoab_respa', 4),
]

labels = [method + ('' if n == 0 else f' (n={n})') for method, n in method_and_n]

mean_error_df = pd.DataFrame(columns=['dt'] + labels)
stdev_error_df = mean_error_df.copy()
for dt in range(10, 101, 10):
    mean_error = []
    stdev_error = []
    for (method, n) in method_and_n:
        df = pd.read_csv(f'n{n}/{method}-{dt}.csv', names=['error', 'q2'], sep='\s+')
        mean_error.append(np.average(df.error.values))
        stdev_error.append(np.std(df.error.values))
    n = len(mean_error_df)
    mean_error_df.loc[n] = [dt] + mean_error
    stdev_error_df.loc[n] = [dt] + stdev_error

fig, ax = plt.subplots(1, 1, figsize=(3.4,2.0))

style = {}
style[0] = '-'
style[1] = '-'
style[2] = '--'
style[4] = '-.'

color = {}
color['nhc_xi_respa'] = 'magenta'
color['baoab_respa'] = 'brown'
color['stochastic_isokinetic_nhc_middle_respa'] = 'blue'
color['stochastic_subkinetic_nhc_middle_respa'] = 'orange'
color['trapezoidal_baoab_respa'] = 'red'
color['perturbed_OU_baoab_respa'] = 'green'

marker = {}
marker['nhc_xi_respa'] = 's'
marker['baoab_respa'] = 'o'
marker['stochastic_isokinetic_nhc_middle_respa'] = '+'
marker['stochastic_subkinetic_nhc_middle_respa'] = '^'
marker['trapezoidal_baoab_respa'] = '>'
marker['perturbed_OU_baoab_respa'] = '<'

for label, (method, n) in zip(labels, method_and_n):
    dt = mean_error_df['dt']
    mean = mean_error_df[label]
    stdev = stdev_error_df[label]
    ax.errorbar(dt, mean, stdev,
                marker=marker[method],
                label=label.replace('_', ' '),
                linestyle=style[n],
                color=color[method])
    # ax.fill_between(dt, mean-stdev, mean+stdev)
ax.set_yscale('log')
# ax.legend()
plt.savefig('linear_resonance')
plt.show()
