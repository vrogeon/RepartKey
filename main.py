import logging
from logging import basicConfig

import Consumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Production in kW
prod = 10.0
initial_prod = prod
# Production used from the autocollect
prod_used = 0.0

keys = { 'partA': Consumer.Consumer('partA',0.5, 10),
         'partB': Consumer.Consumer('partB',0.2, 10),
         'partC': Consumer.Consumer('partC',0.3, 10)
         }

# Function to compute auto consumption
def cal_cons(prod, keys):
    # Use global variables
    global prod_used
    global initial_prod

    # Variable to check if there at least one active consumer
    activ_exist = False

    # First iterates on all consumers to assign consumption according ratio
    for part, cons in keys.items():
        # Manage only active consumers
        if cons.active:
            # Check if consumption from autocollect is going to exceed consumption
            if cons.cons < (cons.colcons + prod * cons.ratio):
                # If this is the case, first de-activate the consumer
                cons.active = False
                # Finally update production used by adding difference between
                # consumption and autocollect consumption
                prod_used += cons.cons - cons.colcons
                # Then set the autocollect consumption to the consumption
                cons.colcons = cons.cons
            else:
                cons.colcons += prod * cons.ratio
                prod_used += prod * cons.ratio
                activ_exist = True

            logger.debug("Consommation de %s est égale à %f", part, cons.colcons)
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

# Start of pogram
cal_cons(prod, keys)

# Print consumption from autocollective
for part, cons in keys.items():
    # printf("Consommation de", part, "est égale à", cons.colcons)
    logger.info("Consommation de %s est égale à %f", part, cons.colcons)