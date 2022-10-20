import copy
from pprint import pprint
from typing import Optional

import numpy as np

from store.kiosk_store import KioskStore
from utils.utils import *
from customers.customer import Customer
from customers.mobile_customer import MobileCustomer
from customers.physical_customer import PhysicalCustomer
from store.queue_store import QueueStore

# Global variable to keep track of current time
NUM_CUSTOMERS_TO_SIMULATE = 300


def randomly_generate_customers():
    customers_list: List[Customer] = []
    for i in range(NUM_CUSTOMERS_TO_SIMULATE):
        customer = random.choices([PhysicalCustomer, MobileCustomer], weights=[8, 2])[0]()
        customers_list.append(customer)
    return customers_list


def simulate_queue_system(input_customers_list):
    curr_time = 0
    # Generate customers
    customers_list = input_customers_list
    # Instantiate physical queue store (i.e. store with original system) and add first customer
    queue_store = QueueStore()
    first_customer = customers_list.pop(0)
    first_customer.arrival_time = 0
    set_orders_creation_times(first_customer.orders, 0)
    queue_store.orders_to_process.extend(first_customer.orders)

    completed_customers = []
    next_customer: Optional[Customer] = None
    while len(completed_customers) < NUM_CUSTOMERS_TO_SIMULATE:
        if next_customer is None:
            next_customer = get_next_customer(customers_list, curr_time)
        if next_customer.arrival_time == curr_time:
            # If it is time for next_customer to arrive, we can pass his orders to the store and get the next customer
            set_orders_creation_times(next_customer.orders, curr_time)
            queue_store.orders_to_process.extend(next_customer.orders)
            # Get the next customer (if there are still customers left) after we have processed the current customer
            if customers_list:
                next_customer = get_next_customer(customers_list, curr_time)

        queue_store.dispatch_orders()
        queue_store.work(curr_time)
        completed_customers.extend(queue_store.release_orders_to_customer(curr_time))
        curr_time += 1

    return completed_customers


def simulate_kiosk_system(input_customers_list, kiosk_count=3):
    curr_time = 0
    # Generate customers
    customers_list = input_customers_list
    # Instantiate kiosk system store
    kiosk_store = KioskStore(num_kiosks=kiosk_count)
    first_customer = customers_list.pop(0)
    first_customer.arrival_time = 0

    kiosk_store.customers_to_process.append(first_customer)

    completed_customers = []
    next_customer: Optional[Customer] = None
    while len(completed_customers) < NUM_CUSTOMERS_TO_SIMULATE:
        if next_customer is None:
            next_customer = get_next_customer(customers_list, curr_time)
        if next_customer.arrival_time == curr_time:
            # If it is time for the next_customer to arrive, we can pass him into the store and get the next customer
            # NOTE: For kiosk system, the order creation time is determined by the kiosk station itself
            kiosk_store.customers_to_process.append(next_customer)
            if customers_list:
                next_customer = get_next_customer(customers_list, curr_time)

        kiosk_store.process_customer_to_kiosk(curr_time)
        kiosk_store.dispatch_all_orders(curr_time)
        kiosk_store.work(curr_time)
        completed_customers.extend(kiosk_store.release_orders_to_customer(curr_time))
        curr_time += 1

    return completed_customers


def extract_average_flow_time(customers: List[Customer]):
    kebab_flow_times = []
    burrito_flow_times = []
    daily_bowl_flow_times = []
    for customer in customers:
        customer_orders = customer.orders
        for order in customer_orders:
            flow_time = order.time_completed - order.time_created
            if order.item_type.__class__.__name__ == 'Kebab':
                kebab_flow_times.append(flow_time)
            if order.item_type.__class__.__name__ == 'Burrito':
                burrito_flow_times.append(flow_time)
            if order.item_type.__class__.__name__ == 'DailyBowl':
                daily_bowl_flow_times.append(flow_time)
    return {'avg_kebab_ft': float(np.mean(kebab_flow_times)),
            'avg_burrito_ft': float(np.mean(burrito_flow_times)),
            'avg_daily_bowl_ft': float(np.mean(daily_bowl_flow_times))}


def extract_physical_customer_avg_wait_time(customers: List[Customer]):
    wait_times = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    for customer in customers:
        if isinstance(customer, PhysicalCustomer):
            try:
                wait_times[customer.qty_ordered].append(customer.time_orders_received - customer.arrival_time)
            except KeyError:
                pass
    res = {}
    for qty, wait_times in wait_times.items():
        if qty <= 6:
            res[qty] = float(np.mean(wait_times))
    return res


def compare_physical_customer_avg_wait_time(data):
    qty_ordered = {i + 1: [None] * 6 for i in range(6)}
    for i, customer_list in enumerate(data):
        num_kiosks = i
        extracted_avg_wait_times = extract_physical_customer_avg_wait_time(customer_list)
        for qty, avg_wait_time in extracted_avg_wait_times.items():
            if qty <= 6:
                qty_ordered[qty][num_kiosks] = avg_wait_time
    return qty_ordered


if __name__ == "__main__":
    customers_list = randomly_generate_customers()
    queue_inputs = copy.deepcopy(customers_list)
    kiosk_inputs = copy.deepcopy(customers_list)

    queue_customers = simulate_queue_system(queue_inputs)
    kiosk_customers = simulate_kiosk_system(kiosk_inputs)

    # TO COMPARE AVERAGE FLOW TIMES BETWEEN SYSTEMS
    # =============================================
    # queue_avg_flow_times = extract_average_flow_time(queue_customers)
    # kiosk_avg_flow_times = extract_average_flow_time(kiosk_customers)
    # plot_chart_1(queue_avg_flow_times, kiosk_avg_flow_times)
    # =============================================

    # TO COMPARE CUSTOMER WAIT TIMES BETWEEN SYSTEMS
    # ==============================================
    # queue_cust_wait_times = extract_physical_customer_avg_wait_time(queue_customers)
    # kiosk_cust_wait_times = extract_physical_customer_avg_wait_time(kiosk_customers)
    # plot_chart_2(queue_cust_wait_times, kiosk_cust_wait_times)
    # ==============================================

    # TO COMPARE AVERAGE CUSTOMER WAITING TIMES AGAINST NUMBER OF KIOSKS FOR KIOSK PROCESS FLOW
    # =========================================================================================
    simulation_inputs = [copy.deepcopy(customers_list) for i in range(6)]
    kiosk_1_results = simulate_kiosk_system(simulation_inputs[0], kiosk_count=1)
    kiosk_2_results = simulate_kiosk_system(simulation_inputs[1], kiosk_count=2)
    kiosk_3_results = simulate_kiosk_system(simulation_inputs[2])
    kiosk_4_results = simulate_kiosk_system(simulation_inputs[3], kiosk_count=4)
    kiosk_5_results = simulate_kiosk_system(simulation_inputs[4], kiosk_count=5)
    kiosk_6_results = simulate_kiosk_system(simulation_inputs[5], kiosk_count=6)
    kiosk_sensitivity_analysis_data = [kiosk_1_results, kiosk_2_results, kiosk_3_results,
                                       kiosk_4_results, kiosk_5_results, kiosk_6_results]
    plot_chart_3_results = compare_physical_customer_avg_wait_time(kiosk_sensitivity_analysis_data)
    plot_chart_3(plot_chart_3_results)
    # =========================================================================================

    # Repeat for 100 simulations
    # WARNING: Time consuming!!!
    # ==================================================================================
    q_results = []
    k_results = []
    for i in range(100):
        customers = randomly_generate_customers()
        q_customers = copy.deepcopy(customers)
        k_customers = copy.deepcopy(customers)
        q_results.append(simulate_queue_system(q_customers))
        k_results.append(simulate_kiosk_system(k_customers))

    # 100 simulations averages and standard deviations for average flow times for each flow unit under each process flow
    # ==================================================================================================================
    q_ft_averages = {'avg_kebab_ft': [], 'avg_burrito_ft': [], 'avg_daily_bowl_ft': []}
    k_ft_averages = {'avg_kebab_ft': [], 'avg_burrito_ft': [], 'avg_daily_bowl_ft': []}
    for result in q_results:
        q_avg_flow_times = extract_average_flow_time(result)
        for key, value in q_avg_flow_times.items():
            q_ft_averages[key].append(value)
    for result in k_results:
        k_avg_flow_times = extract_average_flow_time(result)
        for key, value in k_avg_flow_times.items():
            k_ft_averages[key].append(value)
    q_100_sims_ft_res = {'avg_kebab_ft': {}, 'avg_burrito_ft': {}, 'avg_daily_bowl_ft': {}}
    k_100_sims_ft_res = {'avg_kebab_ft': {}, 'avg_burrito_ft': {}, 'avg_daily_bowl_ft': {}}
    for flow_unit, averages in q_ft_averages.items():
        q_100_sims_ft_res[flow_unit]['mean'] = float(np.mean(averages))
        q_100_sims_ft_res[flow_unit]['s.d.'] = float(np.std(averages))
    for flow_unit, averages in k_ft_averages.items():
        k_100_sims_ft_res[flow_unit]['mean'] = float(np.mean(averages))
        k_100_sims_ft_res[flow_unit]['s.d.'] = float(np.std(averages))
    print('For 100 simulations, average flow times for QUEUE system:')
    pprint(q_100_sims_ft_res)
    print('\nFor 100 simulations, average flow times for KIOSK system:')
    pprint(k_100_sims_ft_res)
    print()
    q_ft_averages_for_chart_1 = {flow_unit: data['mean'] for flow_unit, data in q_100_sims_ft_res.items()}
    k_ft_averages_for_chart_1 = {flow_unit: data['mean'] for flow_unit, data in k_100_sims_ft_res.items()}
    plot_chart_1(q_ft_averages_for_chart_1, k_ft_averages_for_chart_1)
    # ==================================================================================================================

    # 100 simulations averages and standard deviations for average customer waiting times under each system
    # =====================================================================================================
    q_cust_wt_averages = {}
    k_cust_wt_averages = {}
    for result in q_results:
        q_cust_wait_times = extract_physical_customer_avg_wait_time(result)
        for qty_ordered, wait_time in q_cust_wait_times.items():
            if qty_ordered not in q_cust_wt_averages.keys():
                q_cust_wt_averages[qty_ordered] = [wait_time]
            elif not np.isnan(wait_time):
                q_cust_wt_averages[qty_ordered].append(wait_time)
    for result in k_results:
        k_cust_wait_times = extract_physical_customer_avg_wait_time(result)
        for qty_ordered, wait_time in k_cust_wait_times.items():
            if qty_ordered not in k_cust_wt_averages.keys():
                k_cust_wt_averages[qty_ordered] = [wait_time]
            elif not np.isnan(wait_time):
                k_cust_wt_averages[qty_ordered].append(wait_time)
    q_100_sims_cust_wt_res = {i+1: {} for i in range(len(q_cust_wt_averages))}
    k_100_sims_cust_wt_res = {i+1: {} for i in range(len(k_cust_wt_averages))}
    for qty_ordered, averages in q_cust_wt_averages.items():
        q_100_sims_cust_wt_res[qty_ordered]['mean'] = float(np.mean(averages))
        q_100_sims_cust_wt_res[qty_ordered]['s.d.'] = float(np.std(averages))
    for qty_ordered, averages in k_cust_wt_averages.items():
        k_100_sims_cust_wt_res[qty_ordered]['mean'] = float(np.mean(averages))
        k_100_sims_cust_wt_res[qty_ordered]['s.d.'] = float(np.std(averages))
    print('For 100 simulations, average customer waiting times by qty ordered for QUEUE system:')
    pprint(q_100_sims_cust_wt_res)
    print('\nFor 100 simulations, average customer waiting times by qty ordered for KIOSK system:')
    pprint(k_100_sims_cust_wt_res)
    print()
    q_cust_wt_averages_for_chart_1 = {qty_ordered: data['mean'] for qty_ordered, data in q_100_sims_cust_wt_res.items()}
    k_cust_wt_averages_for_chart_1 = {qty_ordered: data['mean'] for qty_ordered, data in k_100_sims_cust_wt_res.items()}
    plot_chart_2(q_cust_wt_averages_for_chart_1, k_cust_wt_averages_for_chart_1)
