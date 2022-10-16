from typing import List, Dict

from customers.customer import Customer
from orders.order import Order


class Store:
    def __init__(self) -> None:
        self.customers_to_process = []
        self.orders_to_process: List[Order] = []
        self.orders_completed: Dict[Customer, List] = {}
