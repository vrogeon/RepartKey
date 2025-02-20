import logging
from logging import basicConfig
import math

import Consumer
import Producer
import Repartition

# Idea 1: Use recursive function to optimize consumption from producers
# Idea 2: Use priority A, B, C... to define consumers that have priority (it can be per producers)
# Idea 3:

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Production in kW
prod = 10.0
initial_prod = prod
# Production used from the autocollect
prod_used = 0.0

keys = { 'partA': Consumer.Consumer('partA', 12345678900001, 0.5, 10),
         'partB': Consumer.Consumer('partB', 12345678900002, 0.2, 10),
         'partC': Consumer.Consumer('partC', 12345678900003, 0.3, 10)
         }

# Function to compute auto consumption
def cal_cons(prod, keys):
    # Use global variables
    global prod_used
    global initial_prod

    # Variable to check if there is at least one active consumer
    activ_exist = False

    # First iterates on all consumers to assign consumption according ratio
    for part, cons in keys.items():
        # Manage only active consumers
        if cons.active:
            # Check if consumption from autocollect is going to exceed consumption
            if cons.cons < (cons.col_cons + prod * cons.ratio):
                # If this is the case, first de-activate the consumer
                cons.active = False
                # Finally update production used by adding difference between
                # consumption and autocollect consumption
                prod_used += cons.cons - cons.col_cons
                # Then set the autocollect consumption to the consumption
                cons.col_cons = cons.cons
            else:
                cons.col_cons += prod * cons.ratio
                prod_used += prod * cons.ratio
                activ_exist = True

            logger.debug("Consommation de %s est égale à %f", part, cons.col_cons)
            logger.debug("Production utilisée: %f", prod_used)

    # If not all the production is used, and at least one consumer still active:
    # compute new ratios
    # and recursively call this function
    if ((prod_used < initial_prod)
            and activ_exist):
        # Sum ratio of all active consumers
        new_sum = 0
        for part, cons in keys.items():
            if cons.active:
                new_sum += cons.ratio

        # Compute new ratios
        for part, cons in keys.items():
            # Manage only active consumers
            if cons.active:
                cons.ratio = cons.ratio / new_sum

        # Call again the function
        cal_cons(initial_prod - prod_used, keys)

    # Compute final ratio for each consumer
    for part, cons in keys.items():
        cons.ratio = cons.col_cons / prod

def cal_cons2(prod, point):

    # Use global variables
    global prod_used
    global initial_prod

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
                prod_used += cons.consumption - cons.auto_consumption
                # Then set the auto_consumption to the consumption
                cons.auto_consumption = cons.consumption
            else:
                # If not, set auto_consumption according the initial ratio
                cons.auto_consumption += prod * cons.key
                prod_used += prod * cons.key
                activ_exist = True

            logger.debug("Consommation est égale à %f", cons.auto_consumption)
            logger.debug("Production utilisée: %f", prod_used)

    # If not all the production is used, and at least one consumer still active:
    # compute new ratios
    # and recursively call this function
    if ((prod_used < initial_prod)
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
        cal_cons2(initial_prod - prod_used, point)

    # Compute final ratio for each consumer
    for cons in point.cons_list:
        cons.key = math.floor(cons.auto_consumption*1000 / initial_prod) / 10


def CalculateRepKey(prod, cons_list, rep):
    global initial_prod

    # First generate list of initial ratio for all consumers
    # rep.GenerateRatioList(cons_list)

    # Build list of points with producer and consumers values:
    #   [prod_slot1, cons1_slot1, cons2_slot1, ..., consN_slot1]
    #   [prod_slot2, cons1_slot2, cons2_slot2, ..., consN_slot2]
    #   ...
    #   [prod_slotX, cons1_slotX, cons2_slotX, ..., consN_slotX]
    # Build list of keys using initial ratio
    i = 0
    for prod_slot in prod.point_list:
        #rep.point_list.append(Repartition.Point(prod_slot.slot, prod_slot.prod))
        rep.AddPointProd(prod_slot.slot, prod_slot.prod)
        for cons in cons_list:
            rep.AddPoint(i, cons.point_list[i].cons, cons.ratio)
            # rep.AddPointCons(i, cons.point_list[i].cons, cons.ratio)
            # rep.AddKeyCons(i,cons.ratio)

        initial_prod = rep.point_list[i].prod
        cal_cons2(initial_prod, rep.point_list[i])

        i += 1




###################### Start of program ######################

# Create list of producers
prod_list = []
prod_list.append(Producer.Producer('Prod1', 1234567901000, 10))

prod_list[0].ReadProduction('Courbe_charge_producteur1.txt')

# Create list of consumers
cons_list = []
cons_list.append(Consumer.Consumer('Cons1',12345678900001, 0.5,10))
cons_list.append(Consumer.Consumer('Cons2',12345678900002, 0.2,10))
cons_list.append(Consumer.Consumer('Cons3',12345678900003, 0.3,10))

cons_list[0].ReadConsumption('Courbe_charge_consommateur1.txt')
cons_list[1].ReadConsumption('Courbe_charge_consommateur2.txt')
cons_list[2].ReadConsumption('Courbe_charge_consommateur3.txt')

# Calculate repartition keys
rep = Repartition.Repartition('Novembre')
CalculateRepKey(prod_list[0],cons_list, rep)

# Simple example
#cal_cons(prod, keys)

# Print consumption from autocollective
for part, cons in keys.items():
    # printf("Consommation de", part, "est égale à", cons.col_cons)
    logger.info("Consommation de %s est égale à %f", part, cons.col_cons)
    logger.info("Ratio de %s est égale à %d%%", part, cons.ratio * 100)