import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

enso = pd.read_csv('~/Documents/GitHub/floodsampling/floodsampling/data/ramesh2017.csv', index_col='year')

# Plot Time Series
enso.loc[10000:12500].plot(
    figsize=(9, 5),
    linewidth=0.5,
    c='blue',
    legend=False,
    grid=True
)
plt.ylabel('NINO3')

plt.savefig('figs/enso.pdf', bbox_inches='tight')