import random
from typing import List

from scipy.stats import norm

from customers.customer import Customer
from main import curr_time
from orders.order import Order


def truncated_norm_dist_rv(min, max, mean, sd):
    min_prob = norm.cdf(min, loc=mean, scale=sd)
    max_prob = norm.cdf(max, loc=mean, scale=sd)
    simulated_prob = (max_prob - min_prob) * random.random() + min_prob
    simulated_qty = norm.ppf(simulated_prob, loc=mean, scale=sd)
    return int(round(simulated_qty, 0))


def set_orders_creation_times(orders_list: List[Order], time_to_set: int):
    for order in orders_list:
        order.time_created = time_to_set


def get_next_customer(list_of_customers: List[Customer]) -> Customer:
    next_customer = list_of_customers.pop(0)
    next_customer.arrival_time = curr_time + next_customer.inter_arrival_time
    return next_customer
