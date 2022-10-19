from store.store import Store
from stations.food_processing_station import FoodProcessingStation
from stations.payment_station import CashierStation


class QueueStore(Store):
    def __init__(self) -> None:
        super().__init__()
        self.wrap_toasting_station = FoodProcessingStation('WrapToastingStation', 8, 12, 10, 2)
        self.salad_base_station = FoodProcessingStation('SaladBaseStation', 3, 18, 12, 5)
        self.sauce_station = FoodProcessingStation('SauceStation', 3, 7, 5, 2)
        self.daily_bowl_toppings_station = FoodProcessingStation('DailyBowlToppingsStation', 5, 20, 13, 5)
        self.meat_station = FoodProcessingStation('MeatStation', 1.5, 5, 3, 1)
        self.additional_toppings_station = FoodProcessingStation('AdditionalToppingsStation', 5, 18, 13, 3)
        self.wrapping_station = FoodProcessingStation('WrappingStation', 3.5, 5, 4, 1.5)
        self.product_toasting_station = FoodProcessingStation('ProductToastingStation', 8, 15, 12, 3, capacity=3)
        self.cashier = CashierStation('Cashier', 15, 35, 18, 6)
        self.process_flow = [self.wrap_toasting_station,
                             self.salad_base_station,
                             self.sauce_station,
                             self.daily_bowl_toppings_station,
                             self.meat_station,
                             self.additional_toppings_station,
                             self.wrapping_station,
                             self.product_toasting_station]

    def dispatch_orders(self):
        """
        Dispatch all orders in the queue to the next respective station in the process flow to work on it.
        """
        if self.orders_to_process:
            self.process_flow[0].queue.extend(self.orders_to_process)
            self.orders_to_process.clear()

    def work(self, curr_time):
        completed_orders = []
        for station in self.process_flow:
            # Queue station requires all orders to pass through every station
            station.queue.extend(completed_orders)
            completed_orders = station.work(curr_time)
        # completed_orders from the final station are completed orders
        self.stage_completed_orders_for_potential_release(completed_orders)

    def release_orders_to_customer(self, curr_time):
        customers_to_process_payment = self.get_customers_with_orders_completed(curr_time)
        self.cashier.queue.extend(customers_to_process_payment)
        released_customers = self.cashier.work(curr_time)
        return released_customers
