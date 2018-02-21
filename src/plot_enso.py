import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from floodsampling.util import get_data_path

data_fname = os.path.join(get_data_path(), 'ramesh2017.csv')
enso = pd.read_csv(data_fname, index_col='year')

# Plot Time Series
enso.loc[10000:12500].plot(
    figsize=(9, 5),
    c='blue',
    linewidth=0.5,
    legend=False,
    grid=True
)
plt.ylabel('NINO3')

plt.savefig('figs/enso.pdf', bbox_inches='tight')