from typing import List

from orders.order import Order


class Station:
    def __init__(self, name, min_time, max_time, mean, sd, capacity=1) -> None:
        self.name = name
        self.processing_time_min = min_time
        self.processing_time_max = max_time
        self.processing_time_mean = mean
        self.processing_time_sd = sd

        self.capacity = capacity
        self.queue: List[Order] = []
        self.curr_orders_processed: List[Order] = []

    def get_processing_time(self):
        from utils.utils import truncated_norm_dist_rv
        return truncated_norm_dist_rv(self.processing_time_min, self.processing_time_max,
                                      self.processing_time_mean, self.processing_time_sd)

    def get_curr_utilization(self):
        return len(self.curr_orders_processed)

    def is_fully_occupied(self):
        curr_utilization = self.get_curr_utilization()
        assert curr_utilization <= self.capacity
        return curr_utilization == self.capacity

    def process_order_from_queue(self, curr_time):
        """
        Add an item from the queue to the list of currently processed orders, updating its completion time
        as well as the capacity of the station itself
        """
        order_to_process = self.queue.pop(0)
        # Get the processing time for the order and update its completion time
        if self.name in order_to_process.item_type.recipe:
            order_to_process.time_completed = curr_time + self.get_processing_time()
        else:
            order_to_process.time_completed = curr_time
        self.curr_orders_processed.append(order_to_process)

    def get_completed_orders(self, curr_time) -> List[Order]:
        """
        Returns a list of orders that are completed within the curr_time provided
        """
        completed_orders = []
        for order in self.curr_orders_processed:
            # Case 1: Order is not completed yet (needs more time to be completed)
            if curr_time < order.time_completed:
                continue
            # Case 2: Order is completed
            else:
                self.curr_orders_processed.remove(order)
                completed_orders.append(order)
        return completed_orders

    def work(self, curr_time) -> List[Order]:
        """
        Adds an order from the queue to the current list of orders being processed (only if there's capacity for it) and
        returns a list of orders that are completed in the current time.
        """
        if not self.is_fully_occupied() and self.queue:
            # If the station is not fully occupied, clear an item from the queue (if it's not empty) and process it
            self.process_order_from_queue(curr_time)
        return self.get_completed_orders(curr_time)
