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

# keys = { 'partA': Consumer.Consumer('partA', 12345678900001, 0.5, 10),
#          'partB': Consumer.Consumer('partB', 12345678900002, 0.2, 10),
#          'partC': Consumer.Consumer('partC', 12345678900003, 0.3, 10)
#          }

###################### Start of program ######################

# Create list of producers
prod_list = []
prod_list.append(Producer.Producer('Prod1', 1234567901000, 10))

prod_list[0].ReadProduction('Courbe_charge_producteur1.txt')

# Create list of consumers
cons_list = []
cons_list.append(Consumer.Consumer('Cons1',12345678900001, 1, 0.5,10))
cons_list.append(Consumer.Consumer('Cons2',12345678900002, 0, 0.2,10))
cons_list.append(Consumer.Consumer('Cons3',12345678900003, 2, 0.3,10))

cons_list[0].ReadConsumption('Courbe_charge_consommateur1.txt')
cons_list[1].ReadConsumption('Courbe_charge_consommateur2.txt')
cons_list[2].ReadConsumption('Courbe_charge_consommateur3.txt')

# Calculate repartition keys
rep = Repartition.Repartition('Novembre')
rep.BuildRep(prod_list[0],cons_list, rep)

rep.WriteRepartitionKey('01112024_30_11_2024.txt')
# Simple example
#cal_cons(prod, keys)

# Print consumption from autocollective
# for part, cons in keys.items():
#     # printf("Consommation de", part, "est égale à", cons.col_cons)
#     logger.info("Consommation de %s est égale à %f", part, cons.col_cons)
#     logger.info("Ratio de %s est égale à %d%%", part, cons.ratio * 100)