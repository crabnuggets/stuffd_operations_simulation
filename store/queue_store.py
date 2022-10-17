from store.store import Store
from stations.base_station import Station


class QueueStore(Store):
    def __init__(self) -> None:
        super().__init__()
        self.wrap_toasting_station = Station('WrapToastingStation',8, 12, 10, 2)
        self.salad_base_station = Station('SaladBaseStation', 3, 18, 12, 5)
        self.sauce_station = Station('SauceStation', 3, 7, 5, 2)
        self.daily_bowl_toppings_station = Station('DailyBowlToppingsStation', 5, 20, 13, 5)
        self.meat_station = Station('MeatStation', 1.5, 5, 3, 1)
        self.additional_toppings_station = Station('AdditionalToppingsStation', 5, 18, 13, 3)
        self.wrapping_station = Station('Wrapping', 3.5, 5, 4, 1.5)
        self.product_toasting_station = Station('ProductToastingStation', 8, 15, 12, 3)
        self.cashier = Station('Cashier', 15, 35, 18, 6)
        self.process_flow = [self.wrap_toasting_station,
                             self.salad_base_station,
                             self.sauce_station,
                             self.daily_bowl_toppings_station,
                             self.meat_station,
                             self.additional_toppings_station,
                             self.wrapping_station,
                             self.product_toasting_station,
                             self.cashier]

    def dispatch_order(self):
        """
        Get the order of the head of the queue and dispatch it to the next respective station to work no it.
        """
        if self.orders_to_process:
            order = self.orders_to_process.pop(0)
            self.process_flow[0].queue.append(order)

    def work(self, curr_time):
        completed_orders = []
        for station in self.process_flow:
            # Queue station requires all orders to pass through every station
            station.queue.extend(completed_orders)
            completed_orders = station.work(curr_time)

        # Orders to progress returns from the final station are completed orders
        # Add completed orders to the store's dictionary of customer orders where customer (key) -> [orders] (value)
        for order in completed_orders:
            customer = order.customer
            if customer not in self.orders_completed:
                self.orders_completed[customer] = [order]
            else:
                self.orders_completed[customer].append(order)

    def release_orders_to_customer(self, curr_time):
        completed_customers = []
        for customer, completed_orders in self.orders_completed.items():
            if len(completed_orders) == customer.qty_ordered:
                customer.time_orders_received = curr_time
                completed_customers.append(customer)
        for customer in completed_customers:
            self.orders_completed.pop(customer)
        return completed_customers
