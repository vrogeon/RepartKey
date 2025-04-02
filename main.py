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


###################### Start of program ######################

# Create list of producers
prod_list = []
prod_list.append(Producer.Producer('Prod1', 1234567901000))
prod_list.append(Producer.Producer('Prod2', 1234567901099))

prod_list[0].read_production('Courbe_charge_producteur1.txt')
prod_list[1].read_production('Courbe_charge_producteur2.txt')

# Create list of consumers
cons_list = []
cons_list.append(Consumer.Consumer('Cons1',12345678900001, [ 0 , 2 ], [ 50 , 10 ]))
cons_list.append(Consumer.Consumer('Cons2',12345678900002, [ 2 , 0 ], [ 20 , 50 ]))
cons_list.append(Consumer.Consumer('Cons3',12345678900003, [ 1 , 0 ], [ 30 , 20 ]))

cons_list[0].read_consumption('Courbe_charge_consommateur1.txt')
cons_list[1].read_consumption('Courbe_charge_consommateur2.txt')
cons_list[2].read_consumption('Courbe_charge_consommateur3.txt')

# Calculate repartition keys
rep = Repartition.Repartition('Novembre')
rep.build_rep(prod_list, cons_list)

rep.write_repartition_key(prod_list)
