# This module is to define Repartition class
import csv

class Repartition:

    # ID of the repartition key
    id
    # List of PRM
    prm = []
    # List of points for each slot of 15 min
    point_list = []


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
        self.id = id
        # self.ratio_list = []
        #self.prm_list = prm_list

    # def GenerateRatioList(self, cons_list):
    #     for cons in cons_list:
    #         self.ratio_list.append(cons.ratio)

    # This function adds production value to the point list
    def AddPointProd(self, slot, prod):
        self.point_list.append(Repartition.Point(slot, prod))

    # This function adds consumption value to the point list
    def AddPointCons(self, index, cons):
        self.point_list[index].cons_list.append(cons)

    # This function adds consumption value to the point list
    def AddPoint(self, index, cons, ratio):
        self.point_list[index].cons_list.append(Repartition.Point.ConsRepart(cons, ratio))

    # This function adds production value to the key list
    # def AddKeyProd(self, slot, prod):
    #     self.key_list.append(Repartition.Point(slot, prod))

    # This function adds consumption key to the key list
    # def AddKeyCons(self, index, ratio):
    #     self.point_list[index].key_list.append(ratio)

    # This function adds repartition value
    # def AddRepart(self,cons_list):
    #     self.point_list.append(cons_list)



    # This function generate file with repartition
    # def SaveRepartFile(self,file):
    #     with open(file, newline='') as csvfile:
    #         next(csvfile) # Skip first line of the file which contains title
    #         cons_file = csv.reader(csvfile,delimiter=';')
    #         for row in cons_file:
    #             self.pointtab.append(Consumer.Point(row[1]))
    #             #print(row)
    #         print('Repartition file created!')

