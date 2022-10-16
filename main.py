from typing import Optional

from utils.utils import *
from customers.customer import Customer
from customers.mobile_customer import MobileCustomer
from customers.physical_customer import PhysicalCustomer
from store.queue_store import QueueStore

# Global variable to keep track of current time
curr_time = 0

if __name__ == "__main__":
    # Generate customers
    customers_list: List[Customer] = []
    for i in range(10):
        customer = random.choices([PhysicalCustomer, MobileCustomer])[0]()
        customers_list.append(customer)

    # Instantiate physical queue store (i.e. store with original system) and add first customer
    queue_store = QueueStore()
    curr_customer = customers_list.pop(0)
    set_orders_creation_times(curr_customer.orders, 0)
    queue_store.orders_to_process.extend(curr_customer.orders)

    next_customer: Optional[Customer] = None

    while customers_list:
        if next_customer is None:
            next_customer = get_next_customer(customers_list, curr_time)
        if next_customer.arrival_time <= curr_time:
            # If it is time for next_customer to arrive, we can pass his orders to the store and get the next customer
            set_orders_creation_times(next_customer.orders, curr_time)
            queue_store.orders_to_process.extend(next_customer.orders)
            next_customer = get_next_customer(customers_list, curr_time)

        queue_store.dispatch_order()
        queue_store.work()
        queue_store.release_orders_to_customer()
        curr_time += 1
