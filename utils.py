import random

from scipy.stats import norm


def truncated_norm_dist_rv(min, max, mean, sd):
    min_prob = norm.cdf(min, loc=mean, scale=sd)
    max_prob = norm.cdf(max, loc=mean, scale=sd)
    simulated_prob = (max_prob - min_prob) * random.random() + min_prob
    simulated_qty = norm.ppf(simulated_prob, loc=mean, scale=sd)
    return round(simulated_qty, 0)
