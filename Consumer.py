# This module is to define Consumer class
import csv

class Consumer:

    # List of points for each slot of 15 min
    point_list = []

    # Define class point to contain specific value for each point
    class Point:
        cons = 0
        # Consumption from autocollective producer
        col_cons = 0
        ratio = 0

        def __init__(self, slot, cons):
            self.slot = slot
            self.cons = cons

    def __init__(self, name, prm, ratio, cons):
        self.name = name
        # Point Reference Mesure
        self.prm = prm
        self.ratio = ratio
        self.cons = cons # Consumption
        self.active = True
        self.point_list = []

    # This function reads a file to set consumption values
    def ReadConsumption(self, file):
        with open(file, newline='') as csvfile:
            next(csvfile) # Skip first line of the file which contains title
            cons_file = csv.reader(csvfile,delimiter=';')
            for row in cons_file:
                self.point_list.append(Consumer.Point(row[0], float(row[1].replace(',','.'))))
                #print(row)
            print('Consumer file read!')

