from typing import List

from customers.customer import Customer
from orders.order import Order
from stations.base_station import Station


class CashierStation(Station):
    def __init__(self, name, min_time, max_time, mean, sd, capacity=1) -> None:
        super().__init__(name, min_time, max_time, mean, sd, capacity)
        self.queue: List[Customer] = []
        self.curr_orders_processed: List[Customer] = []     # In this case, refers to curr_customers_processed

    def process_order_from_queue(self, curr_time):
        """
        Add an item from the queue to the list of currently processed ORDERS, updating its completion time
        as well as the capacity of the station itself
        """
        customer_to_process = self.queue.pop(0)
        # Get the processing time for the order and update its completion time
        completion_time = curr_time + self.get_processing_time()
        customer_to_process.time_orders_received = completion_time
        self.curr_orders_processed.append(customer_to_process)

    def get_completed_orders(self, curr_time) -> List[Customer]:
        """
        Returns a list of CUSTOMERS that have completed payment within the curr_time provided
        """
        released_customers = []
        for customer in self.curr_orders_processed:
            # Case 1: Customer has not completed payment yet (needs more time to be completed)
            if curr_time < customer.time_orders_received:
                continue
            # Case 2: Customer has completed payment
            else:
                self.curr_orders_processed.remove(customer)
                released_customers.append(customer)
        return released_customers


class KioskStation(Station):
    def __init__(self, name, min_time, max_time, mean, sd, capacity=1) -> None:
        super().__init__(name, min_time, max_time, mean, sd, capacity)
        self.queue: List[Customer] = []
        self.curr_orders_processed: List[Customer] = []     # In this case, refers to curr_customers_processed

    def process_order_from_queue(self, curr_time):
        """
        Add an item from the queue to the list of currently processed CUSTOMERS, updating its completion time (i.e. when
        setting the time for the creation of orders) as well as the capacity of the station itself.
        """
        customer_to_process = self.queue.pop(0)
        # Get the processing time for the customer to place an order and make payment and update the creation time for
        # the customer's orders
        completion_time = curr_time + self.get_processing_time()
        for order in customer_to_process.orders:
            order.time_created = completion_time
        self.curr_orders_processed.append(customer_to_process)

    def get_completed_orders(self, curr_time) -> List[Order]:
        """
        Returns a list of orders that a customer has made upon making payment at the kiosk
        """
        released_orders = []
        for customer in self.curr_orders_processed:
            customer_orders = customer.orders
            # Case 1: Order has not been made by the customer (needs more time to be completed and released)
            if curr_time < customer_orders[0].time_created:
                continue
            # Case 2: Order is made by the customer and needs to be released into the process flow
            else:
                self.curr_orders_processed.remove(customer)
                released_orders.extend(customer_orders)
        return released_orders
