from customers.customer import Customer


class MobileCustomer(Customer):
    def __init__(self) -> None:
        super().__init__()
        from utils.utils import truncated_norm_dist_rv

        self.qty_min = 3
        self.qty_max = 10
        self.qty_mean = 5
        self.qty_sd = 2
        self.qty_ordered = truncated_norm_dist_rv(self.qty_min, self.qty_max, self.qty_mean, self.qty_sd)
        self.orders = self.get_flow_units_ordered(self.qty_ordered)
