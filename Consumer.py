# This module is to define consumers class

class Consumer:

    cons = 0
    colcons = 0 # Consumption from autocollective producer

    def __init__(self, name, ratio, cons):
        self.name = name
        self.ratio = ratio
        self.cons = cons # Consumption
        self.active = True

