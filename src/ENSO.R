if(!require(pacman)) install.packages('pacman')
pacman::p_load(dplyr, readr, ggplot2, ggthemes, xts)

# READ THE RAW DATA
raw_file <- '~/Documents/GitHub/floodsampling/floodsampling/data/ramesh2017.csv'
nino <- read_csv(raw_file)

# PLOT EL NINO TIME SERIES
nino_plot <- 
  nino %>%
  filter(year >= 1000 & year < 2000) %>%
  ggplot(aes(x=year, y=nino3)) + 
  geom_line() +
  labs(x='Simulated Year', y='NINO3 Index')

k <- kernel("daniell", m = c(40, 40, 40))
smooth_spec <- spec.pgram(nino$nino3, kernel = k, taper = 0, plot=FALSE)

par(mfrow = c(1, 2))
plot(nino3 ~ year, data=filter(nino, year >= 1000 & year < 2000), main='NINO3 Time Series', type='line', xlab='Year', ylab='NINO3')
plot(smooth_spec, log='no', main='Smoothed Periodogram of NINO3', ylab='Power')
par(mfrow = c(1, 1))