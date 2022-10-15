import random

from flow_units.flow_units import *
from orders.order import *


# Parent class
class Customer:
    def __init__(self) -> None:
        self.inter_arrival_time = random.randint(40, 60)
        self.qty_ordered = None

    def get_flow_units_ordered(self, qty_ordered):
        orders = []
        for i in range(qty_ordered):
            item_to_order = random.choice([Kebab, Burrito, DailyBowl])()
            order = Order(item_to_order)
            orders.append(order)
        return orders
