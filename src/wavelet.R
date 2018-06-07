require(WaveletComp)
require(readr)
require(dplyr)

df <- read_csv('../data/nino3.csv', col_names = c('Year', 'NINO3'))
wc <- WaveletComp::analyze.wavelet(my.data = df, my.series = 'Year', dt=1, make.pval = FALSE, upperPeriod = 2048)

png(filename='../figs/enso_wavelet.png', width=16, height=6, units='in', res=100)
layout(matrix(c(1, 1, 1, 2), nrow=1, ncol=4))
WaveletComp::wt.image(wc, plot.ridge = FALSE, graphics.reset=FALSE)
WaveletComp::wt.avg(wc)
dev.off()
