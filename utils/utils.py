import random

import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np

from typing import List, Dict
from scipy.stats import norm


def truncated_norm_dist_rv(min, max, mean, sd):
    min_prob = norm.cdf(min, loc=mean, scale=sd)
    max_prob = norm.cdf(max, loc=mean, scale=sd)
    simulated_prob = (max_prob - min_prob) * random.random() + min_prob
    simulated_qty = norm.ppf(simulated_prob, loc=mean, scale=sd)
    return int(round(simulated_qty, 0))


def set_orders_creation_times(orders_list, time_to_set: int):
    for order in orders_list:
        order.time_created = time_to_set


def get_next_customer(list_of_customers, curr_time):
    next_customer = list_of_customers.pop(0)
    next_customer.arrival_time = curr_time + next_customer.inter_arrival_time
    return next_customer


def plot_chart_1(queue_data: Dict[str, float], kiosk_data: Dict[str, float]):
    """
    Plots bar chart comparing the flow times of each unit against the different systems
    """
    burrito = (queue_data['avg_burrito_ft'], kiosk_data['avg_burrito_ft'])
    daily_bowl = (queue_data['avg_daily_bowl_ft'], kiosk_data['avg_daily_bowl_ft'])
    kebab = (queue_data['avg_kebab_ft'], kiosk_data['avg_kebab_ft'])

    x_pos = np.arange(len(burrito))

    style.use('ggplot')
    plt.figure(figsize=(10, 10), dpi=1000)

    bar_width = 0.2
    plt.bar(x_pos, burrito, color='royalblue', width=bar_width, label='Burrito')
    plt.bar(x_pos + 0.2, daily_bowl, color='mediumseagreen', width=bar_width, label='Daily bowl')
    plt.bar(x_pos + 0.4, kebab, color='purple', width=bar_width, label='Kebab')
    plt.xticks(x_pos + 0.2, ('Queue', 'Kiosk'), fontsize=11)
    plt.xlabel('Type of process', fontsize=11)
    plt.ylabel('Average flow time (s)', fontsize=11)
    plt.legend(fontsize=11)
    plt.title('Average flow time against type of process', fontsize=11)
    plt.savefig('plots/plot_1.png')


def plot_chart_2(queue_data, kiosk_data):
    """
    Plots line chart for average customer waiting times against their number of orders under the original queue and
    proposed kiosk process flow
    """
    number_of_orders = [1, 2, 3, 4, 5, 6]

    queue_cust_wait_times = [wait_time for qty_ordered, wait_time in queue_data.items()]
    kiosk_cust_wait_times = [wait_time for qty_ordered, wait_time in kiosk_data.items()]

    plt.figure(figsize=(12, 10), dpi=700)

    plt.plot(number_of_orders, kiosk_cust_wait_times, label='Kiosk', color='green')
    plt.plot(number_of_orders, queue_cust_wait_times, label='Queue', color='red')

    plt.xlabel('Number of orders', fontsize=11)
    plt.ylabel('Average waiting time', fontsize=11)
    plt.title('Average waiting time against number of orders', fontsize=11)
    plt.legend()
    plt.savefig('plots/plot_2.png')


def plot_chart_3(kiosk_data: Dict[int, List[float]]):
    """
    Plots line charts for average customer waiting times against number of kiosks under the kiosk process flow
    """
    number_of_kiosks = [i+1 for i in range(6)]
    order_1, order_2, order_3, order_4, order_5, order_6 = [], [], [], [], [], []
    qty_ordered_to_plot_map = {
        1: order_1,
        2: order_2,
        3: order_3,
        4: order_4,
        5: order_5,
        6: order_6
    }
    for qty_ordered, wait_times in kiosk_data.items():
        qty_ordered_to_plot_map[qty_ordered].extend(wait_times)

    plt.figure(figsize=(12, 10), dpi=700)
    plt.plot(number_of_kiosks, order_1, label='1 order', color='green')
    plt.plot(number_of_kiosks, order_2, label='2 order', color='grey', alpha=0.5)
    plt.plot(number_of_kiosks, order_3, label='3 order', color='grey', alpha=0.5)
    plt.plot(number_of_kiosks, order_4, label='4 order', color='grey', alpha=0.5)
    plt.plot(number_of_kiosks, order_5, label='5 order', color='grey', alpha=0.5)
    plt.plot(number_of_kiosks, order_6, label='6 order', color='red')

    plt.xlabel('Number of Kiosks', fontsize=11)
    plt.ylabel('Average waiting time', fontsize=11)
    plt.title('Average waiting time against number of kiosks', fontsize=11)
    plt.legend()
    plt.savefig('plots/plot_3.png')
