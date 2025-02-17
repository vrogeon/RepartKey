# This module is to define Producer class
import csv
class Producer:

    prod = 0
    prod_tab = []

    def __init__(self, name, prod):
        self.name = name
        self.prod = prod # Production
        self.active = True

    # This function reads a file to set prodution values
    def SetProduction(self,file):
        with open(file, newline='') as csvfile:
            next(csvfile) # Skip first line of the file which contains title
            cons_file = csv.reader(csvfile,delimiter=';')
            for row in cons_file:
                self.cons_tab.append( row[1])
                print(row)
            print('Producer file read!')

