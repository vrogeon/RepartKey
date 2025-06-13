# This module is to define Consumer class
import csv

class Consumer:

    # Define class point to contain specific value for each point
    class Point:

        def __init__(self, slot, cons):
            # Timestamp of the slot
            self.slot = slot
            # Consumer consumption for the slot
            self.cons = cons

    def __init__(self, name, prm, priority_list, ratio_list, file = None):
        self.name = name
        # Point Reference Mesure: uniquely identify the consumer
        self.prm = prm
        # List of priority of the consumer for each producer
        self.priority_list = priority_list
        # List of ratio of the consumer for each producer
        self.ratio_list = ratio_list
        # List of points for each slot of 15 min
        self.point_list = []
        if file is not None:
            self.read_consumption(file)

    # This function reads a file to set consumption values
    def read_consumption(self, file):
        with open(file, newline='') as csvfile:
            next(csvfile) # Skip first line of the file which contains title
            cons_file = csv.reader(csvfile,delimiter=';')
            for row in cons_file:
                self.point_list.append(Consumer.Point(row[0], float(row[1].replace(',','.'))))
                #print(row)
            print('Consumer file read!')

