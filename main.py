from pprint import pprint
from typing import Optional

import numpy as np

from utils.utils import *
from customers.customer import Customer
from customers.mobile_customer import MobileCustomer
from customers.physical_customer import PhysicalCustomer
from store.queue_store import QueueStore

# Global variable to keep track of current time
NUM_CUSTOMERS_TO_SIMULATE = 200


def simulate_queue_system():
    curr_time = 0
    # Generate customers
    customers_list: List[Customer] = []
    for i in range(NUM_CUSTOMERS_TO_SIMULATE):
        customer = random.choices([PhysicalCustomer, MobileCustomer], weights=[8, 2])[0]()
        customers_list.append(customer)
    # Instantiate physical queue store (i.e. store with original system) and add first customer
    queue_store = QueueStore()
    first_customer = customers_list.pop(0)
    first_customer.arrival_time = 0
    set_orders_creation_times(first_customer.orders, 0)
    queue_store.orders_to_process.extend(first_customer.orders)

    completed_customers = []
    next_customer: Optional[Customer] = None
    while len(completed_customers) < NUM_CUSTOMERS_TO_SIMULATE:
        if next_customer is None:
            next_customer = get_next_customer(customers_list, curr_time)
        if next_customer.arrival_time == curr_time:
            # If it is time for next_customer to arrive, we can pass his orders to the store and get the next customer
            set_orders_creation_times(next_customer.orders, curr_time)
            queue_store.orders_to_process.extend(next_customer.orders)
            if customers_list:
                next_customer = get_next_customer(customers_list, curr_time)

        queue_store.dispatch_order()
        queue_store.work(curr_time)
        completed_customers.extend(queue_store.release_orders_to_customer(curr_time))
        curr_time += 1

    return completed_customers


def extract_average_flow_time(customers: List[Customer]):
    extracted_orders = [customer.orders for customer in customers]
    flattened_extracted_orders = [order for orders in extracted_orders for order in orders]
    extracted_item_types = [order.item_type.__class__.__name__ for order in flattened_extracted_orders]
    kebab_flow_times = [order.time_completed - order.time_created for order in flattened_extracted_orders
                        if order.item_type.__class__.__name__ == 'Kebab']
    burrito_flow_times = [order.time_completed - order.time_created for order in flattened_extracted_orders
                          if order.item_type.__class__.__name__ == 'Burrito']
    daily_bowl_flow_times = [order.time_completed - order.time_created for order in flattened_extracted_orders
                             if order.item_type.__class__.__name__ == 'DailyBowl']
    return {'avg_kebab_ft': np.mean(kebab_flow_times),
            'avg_burrito_ft': np.mean(burrito_flow_times),
            'avg_daily_bowl_ft': np.mean(daily_bowl_flow_times)}


if __name__ == "__main__":
    queue_customers = simulate_queue_system()
    pprint(extract_average_flow_time(queue_customers))
