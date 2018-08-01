/*
Fit a LN2 Model with a trend on all parameters
*/
data {
  int<lower=0> N;
  int<lower=0> M;
  vector[N] y;
  real mu0_mean; // prior mean on mu
  real mu0_sd; // prior sd on mu
  real beta_mu_mean; // prior mean
  real beta_mu_sd; // prior sd
  real cv_logmean; // log-mean for coefficient of variation
  real cv_logsd; // log-std for coefficient of variation
}
parameters {
  real mu0;
  real beta_mu;
  real<lower=0> sigma0;
  real beta_sigma;
  real coeff_var;
}
model {
  vector[N] mu;
  vector[N] sigma;
  for (n in 1:N){
    mu[n] = mu0 + beta_mu * (n - N);
    sigma[n] = coeff_var * mu[n];
    sigma[n] = sigma[n] >= 0.05 ? sigma[n] : 0.05; // lower limit on sigma
  }
  y ~ lognormal(mu, sigma);
  // regularizing priors
  mu0 ~ normal(mu0_mean, mu0_sd);
  beta_mu ~ normal(beta_mu_mean, beta_mu_sd);
  coeff_var ~ lognormal(cv_logmean, cv_logsd); // reasonable prior on coefficient of variation
}
generated quantities{
  vector[M] yhat;
  vector[M] mu;
  vector[M] sigma;
  for (m in 1:M){
    mu[m] = mu0 + beta_mu * m;
    sigma[m] = coeff_var * mu[m];
    sigma[m] = sigma[m] >= 0.05 ? sigma[m] : 0.05; // lower limit on sigma
    yhat[m] = lognormal_rng(mu[m], sigma[m]);
  }
}
