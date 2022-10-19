import copy
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


def simulate_queue_system(input_customers_list):
    curr_time = 0
    # Generate customers
    customers_list = input_customers_list
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


def simulate_kiosk_system(input_customers_list, kiosk_count=3):
    curr_time = 0
    # Generate customers
    customers_list = input_customers_list
    # Instantiate kiosk system store
    kiosk_store = KioskStore(num_kiosks=kiosk_count)
    first_customer = customers_list.pop(0)
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


def extract_physical_customer_avg_wait_time(customers: List[Customer]):
    wait_times = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    for customer in customers:
        if isinstance(customer, PhysicalCustomer):
            wait_times[customer.qty_ordered].append(customer.time_orders_received - customer.arrival_time)
    res = {}
    for qty, wait_times in wait_times.items():
        res[qty] = np.mean(wait_times)
    return res


def compare_physical_customer_avg_wait_time(data):
    res = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    for customer_list in data:
        extracted_avg_wait_times = extract_physical_customer_avg_wait_time(customer_list)
        for qty, avg_wait_time in extracted_avg_wait_times.items():
            res[qty].append(avg_wait_time)
    return res


if __name__ == "__main__":
    customers_list = randomly_generate_customers()

    # TO COmPARE AVERAGE FLOW TIMES BETWEEN SYSTEMS
    queue_inputs = copy.deepcopy(customers_list)
    kiosk_inputs = copy.deepcopy(customers_list)
    queue_customers = simulate_queue_system(queue_inputs)
    kiosk_customers = simulate_kiosk_system(kiosk_inputs)
    print("Average flow times under QUEUE system:")
    pprint(extract_average_flow_time(queue_customers))
    print("\nAverage flow times under KIOSK system:")
    pprint(extract_average_flow_time(kiosk_customers))
    print("\nAverage customer waiting time for QUEUE system:")
    pprint(extract_physical_customer_avg_wait_time(queue_customers))
    print("\nAverage customer waiting time for KIOSK system:")
    pprint(extract_physical_customer_avg_wait_time(kiosk_customers))

    # TO COMPARE AVERAGE CUSTOMER WAIT TIMES BY VARYING NUMBER OF KIOSKS
    # ==================================================================
    # simulation_inputs = [copy.deepcopy(customers_list) for i in range(6)]
    # kiosk_customers_1 = simulate_kiosk_system(simulation_inputs[0], kiosk_count=1)
    # kiosk_customers_2 = simulate_kiosk_system(simulation_inputs[1], kiosk_count=2)
    # kiosk_customers_3 = simulate_kiosk_system(simulation_inputs[2])
    # kiosk_customers_4 = simulate_kiosk_system(simulation_inputs[3], kiosk_count=4)
    # kiosk_customers_5 = simulate_kiosk_system(simulation_inputs[4], kiosk_count=5)
    # kiosk_customers_6 = simulate_kiosk_system(simulation_inputs[5], kiosk_count=6)
    # results = [kiosk_customers_1, kiosk_customers_2, kiosk_customers_3,
    #            kiosk_customers_4, kiosk_customers_5, kiosk_customers_6]
    # pprint(compare_physical_customer_avg_wait_time(results))
