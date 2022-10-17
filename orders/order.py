from flow_units.base_flow_unit import FlowUnit


class Order:
    def __init__(self, customer, item_type: FlowUnit) -> None:
        self.customer = customer
        self.item_type = item_type
        self.time_created = 0
        self.time_completed = 0
