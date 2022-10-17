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
        pass

    def get_completed_orders(self, curr_time) -> List[Order]:
        pass

    def work(self, curr_time) -> List[Order]:
        """
        Adds an order from the queue to the current list of orders being processed (only if there's capacity for it) and
        returns a list of orders that are completed in the current time.
        """
        if not self.is_fully_occupied() and self.queue:
            # If the station is not fully occupied, clear an item from the queue (if it's not empty) and process it
            self.process_order_from_queue(curr_time)
        return self.get_completed_orders(curr_time)
