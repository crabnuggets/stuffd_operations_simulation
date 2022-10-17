from store.store import Store
from stations.food_processing_station import FoodProcessingStation
from stations.payment_station import PaymentStation


class QueueStore(Store):
    def __init__(self) -> None:
        super().__init__()
        self.wrap_toasting_station = FoodProcessingStation('WrapToastingStation', 8, 12, 10, 2)
        self.salad_base_station = FoodProcessingStation('SaladBaseStation', 3, 18, 12, 5)
        self.sauce_station = FoodProcessingStation('SauceStation', 3, 7, 5, 2)
        self.daily_bowl_toppings_station = FoodProcessingStation('DailyBowlToppingsStation', 5, 20, 13, 5)
        self.meat_station = FoodProcessingStation('MeatStation', 1.5, 5, 3, 1)
        self.additional_toppings_station = FoodProcessingStation('AdditionalToppingsStation', 5, 18, 13, 3)
        self.wrapping_station = FoodProcessingStation('Wrapping', 3.5, 5, 4, 1.5)
        self.product_toasting_station = FoodProcessingStation('ProductToastingStation', 8, 15, 12, 3)
        self.cashier = PaymentStation('Cashier', 15, 35, 18, 6)
        self.process_flow = [self.wrap_toasting_station,
                             self.salad_base_station,
                             self.sauce_station,
                             self.daily_bowl_toppings_station,
                             self.meat_station,
                             self.additional_toppings_station,
                             self.wrapping_station,
                             self.product_toasting_station]

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

    def get_customers_with_orders_completed(self, curr_time):
        completed_customers = []
        for customer, completed_orders in self.orders_completed.items():
            if len(completed_orders) == customer.qty_ordered:
                customer.time_orders_received = curr_time
                completed_customers.append(customer)
        for customer in completed_customers:
            self.orders_completed.pop(customer)
        return completed_customers

    def release_orders_to_customer(self, curr_time):
        customers_to_process_payment = self.get_customers_with_orders_completed(curr_time)
        self.cashier.queue.extend(customers_to_process_payment)
        released_customers = self.cashier.work(curr_time)
        return released_customers
