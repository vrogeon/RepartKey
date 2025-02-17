# This module is to define Consumer class
import csv
class Consumer:

    cons = 0
    cons_tab = []
    colcons = 0 # Consumption from autocollective producer

    def __init__(self, name, ratio, cons):
        self.name = name
        self.ratio = ratio
        self.cons = cons # Consumption
        self.active = True

    # This function reads a file to set consumption values
    def ReadConsumption(self,file):
        with open(file, newline='') as csvfile:
            next(csvfile) # Skip first line of the file which contains title
            cons_file = csv.reader(csvfile,delimiter=';')
            for row in cons_file:
                self.cons_tab.append( row[1])
                #print(row)
            print('Consumer file read!')

