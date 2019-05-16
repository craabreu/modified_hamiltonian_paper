import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import glob
import figstyle
# import itertools
# marker = itertools.cycle(('s', '+', '^', '.', 'o', '*'))

method_and_n = [
    ('SINR', 1),
    ('NHL', 1),
    # ('MOD-V', 1),
    ('MOD', 1),
    ('BAOAB', 1),
    ('SINR', 2),
    ('NHL', 2),
    ('MOD', 2),
    # ('MOD-V', 2),
    ('BAOAB', 2),
    ('SINR', 4),
    ('NHL', 4),
    # ('MOD-V', 4),
    ('MOD', 4),
    ('BAOAB', 4),
]

labels = [method + ('' if n == 0 else f' (n={n})') for method, n in method_and_n]
data = pd.read_csv('water_potential_energy.csv', skipinitialspace=True)

fig, ax = plt.subplots(1, 1, figsize=(3.4,2.0))

style = {}
style[1] = '-'
style[2] = '--'
style[4] = ':'

color = {}
color['SINR'] = 'green'
color['NHL'] = 'orange'
color['MOD-V'] = 'cyan'
color['BAOAB'] = 'red'
color['MOD'] = 'blue'

marker = {}
marker['SINR'] = 'v'
marker['NHL'] = 's'
marker['MOD-V'] = '>'
marker['BAOAB'] = 'o'
marker['MOD'] = '^'

dt = data['dt']
for label, (method, n) in zip(labels, method_and_n):
    mean = data[f'PotEng({method}-L{n})']/512
    stdev = data[f'rmse[PotEng]({method}-L{n})']/512
    p = ax.errorbar(dt, mean, stdev,
                    marker=marker[method],
                    # label=label.replace('_', ' '),
                    linestyle=style[n],
                    color=color[method])
    # ax.fill_between(dt, mean-stdev, mean+stdev)

ax.set_xlabel('Time Step Size (fs)')
ax.set_ylabel('Mean Potential Energy (kJ/mol)')
ax.set_ylim([-43.5, -41])
ax.set_xscale('log')

handles, labels = ax.get_legend_handles_labels()
handles = [h[0] for h in handles] # remove the errorbars
leg = ax.legend(
    handles,
    ['']*8 + ['SIN(R)', 'NHL', 'NHL\\textsuperscript{*}', 'BAOAB'],
    ncol=3,
    columnspacing=0,
    labelspacing=0.2,
    title='n=1~~~n=2~~~n=3',
)
leg._legend_box.align = "left"

# mean = data[f'PotEng(MOD-L1.3)']/512
# stdev = data[f'rmse[PotEng](MOD-L1.3)']/512
# ax.errorbar(dt, mean, stdev)

plt.savefig('water_potential_energy')
plt.show()
