import pandas as pd
import matplotlib.pyplot as plt

enso = pd.read_csv('~/Documents/GitHub/floodsampling/floodsampling/data/ramesh2017.csv', index_col='year')

enso.loc[10000:12500].plot(figsize=(10, 5), linewidth=0.5)
plt.savefig('figs/enso.pdf', bbox_inches='tight')