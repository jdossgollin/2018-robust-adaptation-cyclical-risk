/*
Fit a GEV distribution in stan
Code is largely based on previous code by
Cameron Bracken: http://bechtel.colorado.edu/~bracken/tutorials/stan/
and Yenan Wu: http://discourse.mc-stan.org/t/troubles-in-rejecting-initial-value/1827
*/
functions{
  real gev_lpdf(vector y, real mu, real sigma, real xi) {
    vector[rows(y)] t;
    vector[rows(y)] lp;
    int N;
    N = rows(y);
    for(n in 1:N){
      t[n] = xi==0 ? exp((mu - y[n]) / sigma) : pow(1 + xi * ((y[n] - mu ) / sigma), -1/xi);
      lp[n] = -log(sigma) + (xi + 1) * log(t[n]) - t[n];
    }
    return sum(lp);
  }
}
data {
  int<lower=0> N;
  vector[N] y;
}
parameters {
  real xi;
  real<lower=0> sigma;
  real mu_sigma;
}
model {
  real mu;
  // Priors -- these can be modified depending on your context
  mu_sigma ~ normal(2, 0.5); // prior on ratio of mu to sigma
  xi ~ normal(0, 0.125); // sorta-weakly informative
  // Data Model
  mu = mu_sigma * sigma;
  y ~ gev(mu, sigma, xi);
}
