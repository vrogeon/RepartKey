# This module is to define Repartition class
import csv
import logging
import math

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Repartition:

    # Class to contain specific information for each point
    class Point:

        # Class describing repartition key for all consumer for a specific slot
        class ConsRepart:
            def __init__(self, consumption, ratio):
                self.active = True
                self.consumption = consumption
                # Consumption from autocollect
                self.auto_consumption = 0
                # key represents initial ratio defined, and also intermediate ration computed
                self.key = ratio

        def __init__(self, slot, prod):
            self.slot = slot
            self.prod = prod
            self.cons_list = []

    def __init__(self, id, *prm_list):
        # ID of the repartition key
        self.id = id
        # List of PRM
        self.prm_list = []
        # List of points for each slot of 15 min
        self.point_list = []
        self.prod_used = 0
        self.initial_prod = 0

    # This function adds PRM of consumers
    def AddPrm(self, cons_list):
        for cons in cons_list:
            self.prm_list.append(cons.prm)

    # This function adds production value to the point list
    def AddPointProd(self, slot, prod):
        self.point_list.append(Repartition.Point(slot, prod))

    # This function adds consumption value to the point list
    def AddPointCons(self, index, cons, ratio):
        self.point_list[index].cons_list.append(Repartition.Point.ConsRepart(cons, ratio))

    # Function to calculate repartition keys
    def CalculateRepKey(self, prod, point):

        # Variable to check if there is at least one active consumer
        activ_exist = False

        # First iterates on all consumers to assign consumption according the ratio
        for cons in point.cons_list:
            # Manage only active consumers
            if cons.active:
                # Check if consumption from autocollect is going to exceed consumption
                if cons.consumption < (cons.auto_consumption + prod * cons.key):
                    # If this is the case, first de-activate the consumer
                    cons.active = False
                    # Finally update production used by adding difference between
                    # consumption and auto_consumption
                    self.prod_used += cons.consumption - cons.auto_consumption
                    # Then set the auto_consumption to the consumption
                    cons.auto_consumption = cons.consumption
                else:
                    # If not, set auto_consumption according the initial ratio
                    cons.auto_consumption += prod * cons.key
                    self.prod_used += prod * cons.key
                    activ_exist = True

                # logger.debug("Consommation est égale à %f", cons.auto_consumption)
                # logger.debug("Production utilisée: %f", prod_used)

        # If not all the production is used, and at least one consumer still active:
        # compute new ratios
        # and recursively call this function
        if ((self.prod_used < self.initial_prod)
                and activ_exist):
            # Sum ratio of all active consumers
            new_sum = 0
            for cons in point.cons_list:
                if cons.active:
                    new_sum += cons.key

            # Compute new ratios
            for cons in point.cons_list:
                # Manage only active consumers
                if cons.active:
                    cons.key = cons.key / new_sum

            # Call again the function
            self.CalculateRepKey(self, self.initial_prod - self.prod_used, point)

        # Compute final ratio for each consumer
        for cons in point.cons_list:
            # Use floor function to round to lower value.
            # This ensures that sum of all keys does not exceed 100%
            cons.key = math.floor(cons.auto_consumption * 1000 / self.initial_prod) / 10

    # Function to build repartition
    def BuildRep(self, prod, cons_list, rep):

        # First get list of prm
        self.AddPrm(cons_list)

        # Build for ach time slot the list of points with producer and consumers values:
        #   [prod_slot1, cons1_slot1, cons2_slot1, ..., consN_slot1]
        #   [prod_slot2, cons1_slot2, cons2_slot2, ..., consN_slot2]
        #   ...
        #   [prod_slotX, cons1_slotX, cons2_slotX, ..., consN_slotX]
        # Build list of keys using initial ratio
        i = 0
        for prod_slot in prod.point_list:
            # First add information from production
            self.AddPointProd(prod_slot.slot, prod_slot.prod)
            # Then iterate on each consumer to add its information
            for cons in cons_list:
                # In case production is 0, force consumer information to 0
                # Otherwise add consumers information and calculate repartition keys
                if prod_slot.prod == 0:
                    self.AddPointCons(i, 0, 0)
                else:
                    self.AddPointCons(i, cons.point_list[i].cons, cons.ratio)

            # Compute repartion key only if production is not null
            if prod_slot.prod != 0:
                self.initial_prod = prod_slot.prod
                self.CalculateRepKey(self.initial_prod, self.point_list[i])
            i += 1

    # This function crate file for repartition keys
    def WriteRepartitionKey(self,file):
        with open(file, 'w', newline='') as csvfile:
            keywriter = csv.writer(csvfile,delimiter=';')

            # Add first line with list of PRM
            first_line = []
            first_line.append('Horodate')
            for prm in self.prm_list:
                first_line.append(str(prm))
            keywriter.writerow(first_line)

            # Iterate on each point
            for row in self.point_list:
                # First add information of time slot
                row_key = []
                row_key.append(row.slot)
                # Then add key for each consumer
                for cons in row.cons_list:
                    row_key.append(cons.key)
                keywriter.writerow(row_key)

            print('Repartition key file written !')

