from pprint import pprint
from typing import Optional

import numpy as np

from store.kiosk_store import KioskStore
from utils.utils import *
from customers.customer import Customer
from customers.mobile_customer import MobileCustomer
from customers.physical_customer import PhysicalCustomer
from store.queue_store import QueueStore

# Global variable to keep track of current time
NUM_CUSTOMERS_TO_SIMULATE = 200


def randomly_generate_customers():
    customers_list: List[Customer] = []
    for i in range(NUM_CUSTOMERS_TO_SIMULATE):
        customer = random.choices([PhysicalCustomer, MobileCustomer], weights=[8, 2])[0]()
        customers_list.append(customer)
    return customers_list


def simulate_queue_system():
    curr_time = 0
    # Generate customers
    customers_list = randomly_generate_customers()
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
            # Get the next customer (if there are still customers left) after we have processed the current customer
            if customers_list:
                next_customer = get_next_customer(customers_list, curr_time)

        queue_store.dispatch_orders()
        queue_store.work(curr_time)
        completed_customers.extend(queue_store.release_orders_to_customer(curr_time))
        curr_time += 1

    return completed_customers


def simulate_kiosk_system():
    curr_time = 0
    # Generate customers
    customers_list = randomly_generate_customers()
    # Instantiate kiosk system store
    kiosk_store = KioskStore()
    first_customer = customers_list. pop(0)
    first_customer.arrival_time = 0

    kiosk_store.customers_to_process.append(first_customer)

    completed_customers = []
    next_customer: Optional[Customer] = None
    while len(completed_customers) < NUM_CUSTOMERS_TO_SIMULATE:
        if next_customer is None:
            next_customer = get_next_customer(customers_list, curr_time)
        if next_customer.arrival_time == curr_time:
            # If it is time for the next_customer to arrive, we can pass him into the store and get the next customer
            # NOTE: For kiosk system, the order creation time is determined by the kiosk station itself
            kiosk_store.customers_to_process.append(next_customer)
            if customers_list:
                next_customer = get_next_customer(customers_list, curr_time)

        kiosk_store.process_customer_to_kiosk(curr_time)
        kiosk_store.dispatch_all_orders(curr_time)
        kiosk_store.work(curr_time)
        completed_customers.extend(kiosk_store.release_orders_to_customer(curr_time))
        curr_time += 1

    return completed_customers


def extract_average_flow_time(customers: List[Customer]):
    kebab_flow_times_2 = []
    burrito_flow_times_2 = []
    daily_bowl_flow_times_2 = []
    for customer in customers:
        customer_orders = customer.orders
        for order in customer_orders:
            flow_time = order.time_completed - order.time_created
            if order.item_type.__class__.__name__ == 'Kebab':
                kebab_flow_times_2.append(flow_time)
            if order.item_type.__class__.__name__ == 'Burrito':
                burrito_flow_times_2.append(flow_time)
            if order.item_type.__class__.__name__ == 'DailyBowl':
                daily_bowl_flow_times_2.append(flow_time)
    return {'avg_kebab_ft': np.mean(kebab_flow_times_2),
            'avg_burrito_ft': np.mean(burrito_flow_times_2),
            'avg_daily_bowl_ft': np.mean(daily_bowl_flow_times_2)}


if __name__ == "__main__":
    queue_customers = simulate_queue_system()
    kiosk_customers = simulate_kiosk_system()
    print("Average flow times under QUEUE system:")
    pprint(extract_average_flow_time(queue_customers))
    print("\nAverage flow times under KIOSK system:")
    pprint(extract_average_flow_time(kiosk_customers))
