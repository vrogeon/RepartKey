# This module is to define Repartition class
import csv
import logging
import math
from ast import Param
from tkinter.constants import ACTIVE

import matplotlib.pyplot as plt

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# The following class describes the different states a consumer can have
class State:
    # ACTIVE is the default state.
    # Consumer is used to compute repartition key
    ACTIVE = 1
    # A consumer is INACTIVE when all possible production has been used fot the iteration
    # but its consumption is still not filled
    # Consumer is not used to compute repartition key for the current iteration
    INACTIVE = 2
    # A consumer is COMPLETE when all its consumption has been filled
    # Consumer is not anymore used to compute repartition key for the current time slot
    COMPLETE = 3


def plot_trend(dates, values, title=None):
    """Plot the generated trend"""
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, 'r-')

    if title:
        plt.title(title)
    else:
        plt.title(f"Trend")

    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return plt

class Repartition:

    # Class to contain specific information for each point
    class Point:

        # Class containing producer information to compute repartition keys
        class ProdRepart:
            def __init__(self, initial_production):
                self.initial_production = initial_production
                self.production = initial_production
                self.prod_to_remove = 0

        # Class describing repartition keys for all consumers for a specific slot
        class ConsRepart:
            class Param:
                def __init__(self, priority, ratio):
                    # Consumption from autocollect
                    self.auto_consumption = 0
                    # List of priorities for each consumer
                    self.priority = priority
                    # List representing key and intermediate ratio computed for each producer
                    self.key = ratio

            def __init__(self, consumption, priority_list, ratio_list):
                # Represents state of the consumer
                self.state = State.ACTIVE
                self.consumption = consumption
                # List of consumption parameters for each producer
                self.param_list = []
                for priority, ratio in zip(priority_list, ratio_list):
                    self.param_list.append(Repartition.Point.ConsRepart.Param(priority, ratio))

        def __init__(self, slot):
            self.slot = slot
            self.prod_list = []
            self.cons_list = []

    def __init__(self, *prm_list):
        # List of PRM
        self.prm_list = []
        # List of points for each slot of 15 min
        self.point_list = []

    # This function adds PRM of consumers
    def add_prm(self, cons_list):
        for cons in cons_list:
            self.prm_list.append(cons.prm)

    # This function adds point with slot information
    def add_point(self, slot):
        self.point_list.append(Repartition.Point(slot))

    # This function adds production value to the point list
    def add_point_prod(self, index, prod):
        self.point_list[index].prod_list.append(Repartition.Point.ProdRepart(prod))

    # This function adds consumption value to the point list
    def add_point_cons(self, index, cons, priority, ratio):
        self.point_list[index].cons_list.append(Repartition.Point.ConsRepart(cons, priority, ratio))

    # This function returns true if at least one consumer is active
    def are_consumers_active(self, point):
        active = False
        for cons in point.cons_list:
            # if cons.active:
            if cons.state == State.ACTIVE:
                active = True
        return active

    # Function to calculate repartition keys
    def calculate_rep_key(self, current_priority, point):

        # self.count += 1
        # print('count = ', self.count)

        # Variable to check if there is at least one consumer with current priority
        priority_exist = False

        # First iterates on all consumers to assign consumption according the ratio
        for cons in point.cons_list:

            # Check if consumer has the current priority for one of the producer
            for param in cons.param_list:
                if param.priority == current_priority:
                    priority_exist = True

            # Manage only enabled consumers and matching current priority
            if cons.state == State.ACTIVE:
                if priority_exist == True:

                    prod_total = 0
                    for param, prod in zip(cons.param_list, point.prod_list):
                        if param.priority == current_priority:
                            prod_total += (prod.production * param.key) / 100

                    # No production to use anymore with this priority => de-activate the consumer
                    if prod_total == 0:
                        cons.state = State.INACTIVE

                    # Get current auto_consumption used from all producers
                    auto_consumption_total = 0
                    for param in cons.param_list:
                            auto_consumption_total += param.auto_consumption

                    # Check if consumption from autocollect is going to exceed consumption
                    if cons.consumption < (prod_total + auto_consumption_total):
                        # If this is the case, set consumer to COMPLETE state
                        cons.state = State.COMPLETE

                        # Sum key to get new ratio
                        key_total = 0
                        for param in cons.param_list:
                            if param.priority == current_priority:
                                key_total += param.key

                        # Loop on all param to add consumption for consumer
                        for param, prod in zip(cons.param_list, point.prod_list):
                            if param.priority == current_priority:
                                # Compute the new production by first getting part of production using the key,
                                # then applying ratio using remaining consumption compared to total production.
                                new_prod = prod.production * (param.key / 100) * ((cons.consumption - auto_consumption_total) / prod_total)
                                param.auto_consumption += new_prod
                                prod.prod_to_remove += new_prod

                    else:
                        # If not, set auto_consumption according to the initial ratio
                        for param, prod in zip(cons.param_list, point.prod_list):
                            if param.priority == current_priority:
                                new_prod = (param.key * prod.production) / 100
                                prod.prod_to_remove += new_prod
                                param.auto_consumption += new_prod

                    # logger.debug("Consommation est égale à %f", cons.auto_consumption)
                    # logger.debug("Production utilisée: %f", prod_used)
                else:
                    cons.state = State.INACTIVE


        # Refresh production by removing what has been consumed by consumers
        for prod in point.prod_list:
            prod.production -= prod.prod_to_remove
            prod.prod_to_remove = 0

        # Get total production available
        prod_total = 0
        for prod in point.prod_list:
            prod_total += prod.production

        # If not all the production is used, and at least one consumer still enabled:
        # compute new ratios
        # and recursively call this function
        if ( (prod_total > 0)
            and self.are_consumers_active(point)
            and priority_exist):

            # Sum ratio of all enabled consumers
            new_sum = []
            index_prod = 0
            for prod in point.prod_list:
                new_sum.append(0)
                for cons in point.cons_list:
                    if (cons.state == State.ACTIVE and
                        cons.param_list[index_prod].priority == current_priority):
                        new_sum[index_prod] +=  cons.param_list[index_prod].key
                index_prod += 1

            # Compute new ratios
            for cons in point.cons_list:
                # Manage only enabled consumers
                if cons.state == State.ACTIVE:
                    index_param = 0
                    for param in cons.param_list:
                        if param.priority == current_priority:
                            param.key = (100 * param.key) / new_sum[index_param]
                        index_param += 1

            # Call again the function
            self.calculate_rep_key(current_priority, point)

        # Reactivate consumer for next iteration
        if not self.are_consumers_active(point):
            for cons in point.cons_list:
                if cons.state == State.INACTIVE:
                    cons.state = State.ACTIVE

        if priority_exist:
            # increase priority
            current_priority += 1
            # Call again the function
            self.calculate_rep_key(current_priority, point)

        # Compute final ratio for each consumer
        for cons in point.cons_list:
            index_param = 0
            for param in cons.param_list:
                # self.count += 1
                # print('count = ', self.count)

                # Use floor function to round to lower value.
                # This ensures that sum of all keys does not exceed 100%
                param.key = math.floor(param.auto_consumption * 1000 / point.prod_list[index_param].initial_production) / 10
                index_param += 1

    # Function to build repartition
    def build_rep(self, prod_list, cons_list):

        # First get list of prm
        self.add_prm(cons_list)

        # Build for each time slot the list of points with producer and consumers values:
        #   [prod_slot1, cons1_slot1, cons2_slot1, ..., consN_slot1]
        #   [prod_slot2, cons1_slot2, cons2_slot2, ..., consN_slot2]
        #   ...
        #   [prod_slotX, cons1_slotX, cons2_slotX, ..., consN_slotX]
        # Build list of keys using initial ratio
        i = 0
        self.count = 0
        for prod_slot in prod_list[0].point_list:

            # First add slot
            self.add_point(prod_slot.slot)

            # Populate producer list
            for producer in prod_list:
                self.add_point_prod(i, producer.point_list[i].prod)

            # Then iterate on each consumer to add its information
            for cons in cons_list:
                # In case production is 0, force consumer information to 0
                # Otherwise add consumers information and calculate repartition keys
                if producer.point_list[i].prod == 0:
                    null_ratio_list = [0 for i in range(0, len(cons.ratio_list))]
                    self.add_point_cons(i, cons.point_list[i].cons, cons.priority_list, null_ratio_list)
                else:
                    self.add_point_cons(i, cons.point_list[i].cons, cons.priority_list, cons.ratio_list)

            # Compute repartition keys only if production is not null
            if prod_slot.prod != 0:
            # self.count = 0
                self.calculate_rep_key(0, self.point_list[i])
            i += 1

    # This function create files for repartition keys
    def write_repartition_key(self, prod_list):
        index_prod = 0
        for prod in prod_list:
            file = str(prod.prm) + '.csv'
            with open(file, 'w', newline='') as csvfile:
                keywriter = csv.writer(csvfile,delimiter=';')

                # Add first line with list of PRM
                first_line = []
                first_line.append('Horodate')
                for prm in self.prm_list:
                    first_line.append(str(prm))

                # Start the debug information at the second line
                line_for_debug_info = 1
                first_line.append('TOTAL')
                first_line.append('=NB.SI(F2:F2881;"NOK")')
                line_for_debug_info += 1

                keywriter.writerow(first_line)

                # Iterate on each point
                for row in self.point_list:
                    # First add information of time slot
                    row_key = []
                    row_key.append(row.slot)
                    # Then add key for each consumer
                    for cons in row.cons_list:
                        # Use this line to print float with ',' instead of '.'
                        row_key.append(str(cons.param_list[index_prod].key).replace('.', ','))
                        # row_key.append(cons.param_list[index_prod].key)

                    # Add check information for excel
                    line = '=SOMME(SUBSTITUE(B'+str(line_for_debug_info)+';".";",");'\
                            'SUBSTITUE(C'+str(line_for_debug_info)+';".";",");'\
                            'SUBSTITUE(D'+str(line_for_debug_info)+';".";","))'
                    row_key.append(line)
                    line = '=SI(E'+str(line_for_debug_info)+'>100;"NOK";"")'
                    row_key.append(line)
                    line_for_debug_info += 1

                    keywriter.writerow(row_key)

                print('Repartition key file written !')

                index_prod += 1


    # This function create files for repartition keys
    def generate_graph(self, prod_list, cons_list):
        index_prod = 0
        for prod in prod_list:
            file = str(prod.prm) + '_graph.csv'
            with open(file, 'w', newline='') as csvfile:
                keywriter = csv.writer(csvfile,delimiter=';')

                # Add first line with name of consumers
                first_line = []
                first_line.append('Horodate')
                first_line.append(prod.name + '_production')
                for cons in cons_list:
                    first_line.append(cons.name + '_cons')
                    first_line.append(cons.name + '_auto_cons')
                    first_line.append(cons.name + '_auto_prod rate')

                first_line.append('auto_cons rate')

                keywriter.writerow(first_line)

                # Plot trends
                plt.figure(figsize=(12, 6))

                plot_slot = []
                plot_value = []

                # Iterate on each point
                for row in self.point_list:
                    # First add information of time slot
                    row_key = []
                    row_key.append(row.slot)
                    row_key.append(str(row.prod_list[index_prod].initial_production).replace('.', ','))

                    plot_slot.append(row.slot)

                    total_auto_consumption = 0

                    # Then add key for each consumer
                    for cons in row.cons_list:
                        row_key.append(str(cons.consumption).replace('.', ','))
                        # Use this line to print float with ',' instead of '.'
                        auto_cons = row.prod_list[index_prod].initial_production * cons.param_list[index_prod].key
                        auto_cons = math.floor(auto_cons) / 100
                        row_key.append(str(auto_cons).replace('.', ','))
                        # row_key.append(cons.param_list[index_prod].key)

                        # Add auto production rate
                        if (cons.consumption != 0):
                            row_key.append(str(int(auto_cons * 100 / cons.consumption)).replace('.', ','))
                        else:
                            row_key.append(0)

                        # Multiply by 100 and force to int to prevent having float representation issues
                        total_auto_consumption += int(round(cons.param_list[index_prod].auto_consumption * 100))

                    # Write auto consumption ratio
                    if row.prod_list[index_prod].initial_production != 0:
                        auto_cons_ratio = int(total_auto_consumption  / row.prod_list[index_prod].initial_production)
                    else:
                        auto_cons_ratio = 0

                    row_key.append(auto_cons_ratio)
                    plot_value.append(auto_cons_ratio)

                    keywriter.writerow(row_key)

                    # if "23:45" in row.slot:
                    #     title = row.slot[:10]
                    #     plot_trend(plot_slot, plot_value, title)
                    #     plot_slot = []
                    #     plot_value = []

                plot_trend(plot_slot, plot_value)
                print('Repartition key file written !')

                plt.show()

                index_prod += 1