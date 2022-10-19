from store.store import Store
from customers.physical_customer import PhysicalCustomer
from stations.food_processing_station import FoodProcessingStation
from stations.payment_station import KioskStation


class KioskStore(Store):
    def __init__(self, num_kiosks=3) -> None:
        super().__init__()
        self.wrap_toasting_station = FoodProcessingStation('WrapToastingStation', 8, 12, 10, 2)
        self.salad_base_station = FoodProcessingStation('SaladBaseStation', 2, 6, 4, 2)
        self.sauce_station = FoodProcessingStation('SauceStation', 1, 3, 2, 0.5)
        self.daily_bowl_toppings_station = FoodProcessingStation('DailyBowlToppingsStation', 3, 7, 5, 1)
        self.meat_station = FoodProcessingStation('MeatStation', 1.5, 3, 2, 0.5)
        self.additional_toppings_station = FoodProcessingStation('AdditionalToppingsStation', 2, 5, 3.5, 1)
        self.wrapping_station = FoodProcessingStation('WrappingStation', 3.5, 5, 4, 1.5)
        self.product_toasting_station = FoodProcessingStation('ProductToastingStation', 8, 15, 12, 3)
        self.kiosk = KioskStation('Kiosk', 35, 130, 60, 40, capacity=num_kiosks)
        self.process_flow = [self.wrap_toasting_station,
                             self.salad_base_station,
                             self.sauce_station,
                             self.daily_bowl_toppings_station,
                             self.meat_station,
                             self.additional_toppings_station,
                             self.wrapping_station,
                             self.product_toasting_station]
        self.station_dispatch_map = {station.name: station for station in self.process_flow}

    def process_customer_to_kiosk(self, curr_time):
        """
        Pop a customer from the queue and add the customer to the kiosk queue
        """
        if self.customers_to_process:
            customer = self.customers_to_process.pop(0)
            if isinstance(customer, PhysicalCustomer):
                self.kiosk.queue.append(customer)
            else:
                for order in customer.orders:
                    order.time_created = curr_time
                    self.dispatch_order(order)

    def dispatch_order(self, order):
        # Dispatch each order to its first respective station
        order_recipe = order.item_type.recipe
        # Progress the stage in production of the flow unit and get the station for it
        station_to_dispatch = order_recipe[order.item_type.curr_stage_in_production]
        order.item_type.curr_stage_in_production += 1
        self.station_dispatch_map[station_to_dispatch].queue.append(order)

    def dispatch_all_orders(self, curr_time):
        """
        Process the kiosk and get any orders that have been created by customers who have completed their order at it.
        Dispatch these orders to their respective first stations
        """
        released_orders = self.kiosk.work(curr_time)
        for order in released_orders:
            self.dispatch_order(order)

    def work(self, curr_time):
        completed_orders = []
        for station in self.process_flow:
            # Kiosk stations dispatches completed orders to stations based on flow unit's recipes
            orders_to_progress = station.work(curr_time)
            for order in orders_to_progress:
                # If there are remaining stations for the order to go through, dispatch it. Else, the order is complete
                if order.item_type.curr_stage_in_production < len(order.item_type.recipe):
                    self.dispatch_order(order)
                else:
                    completed_orders.append(order)

        # completed_orders from the final station are also completed orders
        self.stage_completed_orders_for_potential_release(completed_orders)

    def release_orders_to_customer(self, curr_time):
        customers_to_release_orders_to = self.get_customers_with_orders_completed(curr_time)
        for customer in customers_to_release_orders_to:
            customer.time_orders_received = curr_time
        return customers_to_release_orders_to


