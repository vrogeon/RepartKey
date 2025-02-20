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
            # List of key computed
            # self.key_list = []

    def __init__(self, id, *prm_list):
        # ID of the repartition key
        self.id = id
        # List of PRM
        self.prm = []
        # List of points for each slot of 15 min
        self.point_list = []

    # This function adds production value to the point list
    def AddPointProd(self, slot, prod):
        self.point_list.append(Repartition.Point(slot, prod))

    # This function adds consumption value to the point list
    def AddPoint(self, index, cons, ratio):
        self.point_list[index].cons_list.append(Repartition.Point.ConsRepart(cons, ratio))
