import random
from typing import List

from flow_units.flow_units import *
from orders.order import *


# Parent class
class Customer:
    def __init__(self) -> None:
        self.inter_arrival_time = random.randint(40, 60)
        self.arrival_time = None
        self.qty_ordered = None
        self.orders: List[Order] = []
        self.time_orders_received = None

    def get_flow_units_ordered(self, qty_ordered):
        orders = []
        for i in range(qty_ordered):
            item_to_order = random.choice([Kebab, Burrito, DailyBowl])()
            order = Order(self, item_to_order)
            orders.append(order)
        return orders
