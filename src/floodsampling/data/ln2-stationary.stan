/*
Fit a stationary LN2 Model
*/
data {
  int<lower=0> N;
  int<lower=0> M;
  vector[N] y;
  real mu_mean; // prior mean on mu
  real mu_sd; // prior sd on mu
  real sigma_mean; // prior mean on sigma
  real sigma_sd; // prior sd on sigma
}
transformed data {
  vector[N] Q; // log streamflow
  for (n in 1:N){
    Q[n] = log(y[n]);
  }
}
parameters {
  real mu;
  real<lower=0> sigma;
}
model {
  Q ~ normal(mu, sigma);
  // priors are passed as data
  mu ~ normal(mu_mean, mu_sd);
  sigma ~ normal(sigma_mean, sigma_sd);
}
generated quantities{
  vector[M] yhat;
  for (m in 1:M){
    yhat[m] = normal_rng(mu, sigma);
  }
}
