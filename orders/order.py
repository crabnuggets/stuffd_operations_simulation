class Order:
    def __init__(self, item_type) -> None:
        self.item_type = item_type
        self.time_created = None
        self.time_completed = None
