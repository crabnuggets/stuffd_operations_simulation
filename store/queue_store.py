from store.store import Store
from stations.IRL_stations import *


class QueueStore(Store):
    def __init__(self) -> None:
        super().__init__()
        self.wrap_toasting_station = IRLWrapToastingStation()
        self.salad_base_station = IRLSaladBaseStation()
        self.sauce_station = IRLSauceStation()
        self.daily_bowl_toppings_station = IRLDailyBowlToppingsStation()
        self.meat_station = IRLMeatStation()
        self.additional_toppings_station = IRLAdditionalToppingsStation()
        self.product_toasting_station = IRLProductToastingStation()
        self.cashier = IRLPaymentStation()
        self.process_flow = [self.wrap_toasting_station,
                             self.salad_base_station,
                             self.sauce_station,
                             self.daily_bowl_toppings_station,
                             self.meat_station,
                             self.additional_toppings_station,
                             self.product_toasting_station,
                             self.cashier]

    def process_customer(self):
        """
        Add the orders from the customer at the head of the queue (if one exists) to the list of orders to process.
        """
        if self.customers_to_process:
            customer = self.customers_to_process.pop(0)
            self.orders_to_process.extend(customer.orders)

    def dispatch_order(self):
        """
        Get the order of the head of the queue and dispatch it to the next respective station to work no it.
        """
        if self.orders_to_process:
            order = self.orders_to_process.pop(0)
            self.process_flow[0].queue.append(order)
