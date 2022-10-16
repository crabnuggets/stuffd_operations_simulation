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
