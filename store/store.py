from typing import List, Dict

from customers.customer import Customer
from orders.order import Order


class Store:
    def __init__(self) -> None:
        self.customers_to_process = []
        self.orders_to_process: List[Order] = []
        self.orders_completed: Dict[Customer, List] = {}

    def stage_completed_orders_for_potential_release(self, completed_orders):
        # Add completed orders to the store's dictionary of customer orders where customer (key) -> [orders] (value)
        for order in completed_orders:
            # Get the customer that made the order
            customer = order.customer
            if customer not in self.orders_completed:
                self.orders_completed[customer] = [order]
            else:
                self.orders_completed[customer].append(order)

    def get_customers_with_orders_completed(self, curr_time):
        completed_customers = []
        for customer, completed_orders in self.orders_completed.items():
            if len(completed_orders) == customer.qty_ordered:
                customer.time_orders_received = curr_time
                completed_customers.append(customer)
        for customer in completed_customers:
            self.orders_completed.pop(customer)
        return completed_customers
