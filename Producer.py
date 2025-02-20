# This module is to define Producer class
import csv
from calendar import prmonth

class Producer:

    # Define class point to contain specific value for each point
    class Point:
        # prod = 0

        def __init__(self, slot, prod):
            self.slot = slot
            self.prod = prod
            
    def __init__(self, name, prm, prod):
        self.name = name
        self.prm = prm
        self.prod = prod # Production
        self.point_list = []

    # This function reads a file to set production values
    def ReadProduction(self,file):
        with open(file, newline='') as csvfile:
            next(csvfile) # Skip first line of the file which contains title
            cons_file = csv.reader(csvfile,delimiter=';')
            for row in cons_file:
                self.point_list.append(Producer.Point(row[0], float(row[1].replace(',','.'))))
                # print(row)
            print('Producer file read!')

