import random

from scipy.stats import norm


# Parent class
class Customer:
    def __init__(self) -> None:
        self.inter_arrival_time = random.randint(40, 60)
        self.qty_ordered = None

    def __get_flow_units_ordered(self, qty_ordered):
        orders = []
        for i in range(qty_ordered):
            orders.append(random.choice(['Kebab', 'Burrito', 'DailyBowl']))
        return orders
