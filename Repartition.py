# This module is to define Repartition class
import csv

class Repartition:

    # Class to contain specific information for each point
    class Point:
        slot = 0
        prod = 0

        # Class
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