from typing import List

from orders.order import Order
from stations.base_station import Station


class FoodProcessingStation(Station):
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


