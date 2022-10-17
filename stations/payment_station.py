from typing import List

from customers.customer import Customer
from orders.order import Order
from stations.base_station import Station


class PaymentStation(Station):
    def __init__(self, name, min_time, max_time, mean, sd, capacity=1) -> None:
        super().__init__(name, min_time, max_time, mean, sd, capacity)
        self.queue: List[Customer] = []
        self.curr_orders_processed: List[Customer] = []

    def process_order_from_queue(self, curr_time):
        """
        Add an item from the queue to the list of currently processed orders, updating its completion time
        as well as the capacity of the station itself
        """
        customer_to_process = self.queue.pop(0)
        # Get the processing time for the order and update its completion time
        completion_time = curr_time + self.get_processing_time()
        customer_to_process.time_orders_received = completion_time
        for order in customer_to_process.orders:
            order.time_completed = completion_time
        self.curr_orders_processed.append(customer_to_process)

    def get_completed_orders(self, curr_time) -> List[Customer]:
        """
        Returns a list of orders that are completed within the curr_time provided
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

