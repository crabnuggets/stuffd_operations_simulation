from customers.customer import Customer
from flow_units.base_flow_unit import FlowUnit


class Order:
    def __init__(self, customer: Customer, item_type: FlowUnit) -> None:
        self.customer = customer
        self.item_type = item_type
        self.time_created = None
        self.time_completed = None
