/*
Fit a LN2 Model with a trend on all parameters
*/
data {
  int<lower=0> N;
  int<lower=0> M;
  vector[N] y;
  real mu0_mean; // prior mean on mu
  real mu0_sd; // prior sd on mu
  real sigma0_mean; // prior mean on sigma
  real sigma0_sd; // prior sd on sigma
  real beta_mu_mean; // prior mean
  real beta_mu_sd; // prior sd
  real beta_sigma_mean; // prior mean
  real beta_sigma_sd; // prior sd
}
transformed data {
  vector[N] Q; // log streamflow
  for (n in 1:N){
    Q[n] = log(y[n]);
  }
}
parameters {
  real mu0;
  real beta_mu;
  real<lower=0> sigma0;
  real beta_sigma;
}
model {
  vector[N] mu;
  vector[N] sigma;
  for (n in 1:N){
    mu[n] = mu0 + beta_mu * (n - N);
    sigma[n] = sigma0 + beta_sigma * (n - N);
    sigma[n] = sigma[n] >= 0.05 ? sigma[n] : 0.05; // lower limit on sigma
  }
  Q ~ normal(mu, sigma);
  // regularizing priors
  beta_mu ~ normal(beta_mu_mean, beta_mu_sd);
  beta_sigma ~ normal(beta_sigma_mean, beta_sigma_sd);
  mu0 ~ normal(mu0_mean, mu0_sd);
  sigma0 ~ normal(sigma0_mean, sigma0_sd);
}
generated quantities{
  vector[M] yhat;
  vector[M] mu;
  vector[M] sigma;
  for (m in 1:M){
    mu[m] = mu0 + beta_mu * m;
    sigma[m] = sigma0 + beta_sigma * m;
    sigma[m] = sigma[m] >= 0.05 ? sigma[m] : 0.05; // lower limit on sigma
    yhat[m] = normal_rng(mu[m], sigma[m]);
  }
}
