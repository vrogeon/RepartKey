import logging
from logging import basicConfig
import math

import Consumer
import Producer
import Repartition

# Idea 1: Use recursive function to optimize consumption from producers
# Idea 2: Use priority 0, 1 ,2... to define consumers that have priority (it can be per producers)
# Idea 3:

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


###################### Start of program ######################

# Create list of producers
prod_list = []
# prod_list.append(Producer.Producer('Prod2', 1234567901099))
prod_list.append(Producer.Producer('Prod1', 1234567901000))

# prod_list[1].read_production('Courbe_charge_producteur2.txt')
# prod_list[0].read_production('Simulation_AntonySoleil\\Simu_Prod.csv')
prod_list[0].read_production('Releve_AntonySoleil\\Simu_Prod_Soli_75.csv')

# Create list of consumers
cons_list = []
# cons_list.append(Consumer.Consumer('Cons1',12345678900001, [ 0 , 2 ], [ 50 , 10 ]))
# cons_list.append(Consumer.Consumer('Cons2',12345678900002, [ 2 , 0 ], [ 20 , 50 ]))
# cons_list.append(Consumer.Consumer('Cons3',12345678900003, [ 1 , 0 ], [ 30 , 20 ]))

# cons_list.append(Consumer.Consumer('5Conso','5Conso',                               [ 0 ], [ 2 ]))
# cons_list.append(Consumer.Consumer('Azimut','Azimut',                               [ 0 ], [ 3 ]))
# cons_list.append(Consumer.Consumer('Harmony2','Harmony2',                           [ 0 ], [ 20 ]))
# cons_list.append(Consumer.Consumer('HautDeBievreHabitat12','HautDeBievreHabitat12', [ 0 ], [ 28 ]))
# cons_list.append(Consumer.Consumer('HautDeBievreHabitat3','HautDeBievreHabitat3',   [ 0 ], [ 20 ]))
# cons_list.append(Consumer.Consumer('PtiteEchoppe','PtiteEchoppe',                   [ 0 ], [ 27 ]))

# cons_list.append(Consumer.Consumer('Parking_Harmony2','Parking_Harmony2',[ 0 ], [ 20 ]))
cons_list.append(Consumer.Consumer('Habitat_Humanisme','Habitat_Humanisme',[ 0 ], [ 2 ]))
cons_list.append(Consumer.Consumer('1ParvisDuBreuil','1ParvisDuBreuil', [ 0 ], [ 28 ]))
cons_list.append(Consumer.Consumer('2ParvisDuBreuil','2ParvisDuBreuil', [ 0 ], [ 28 ]))
cons_list.append(Consumer.Consumer('3ParvisDuBreuil','3ParvisDuBreuil', [ 0 ], [ 28 ]))
cons_list.append(Consumer.Consumer('2ParvisDeLaBievre','2ParvisDeLaBievre', [ 0 ], [ 28 ]))
cons_list.append(Consumer.Consumer('3ParvisDeLaBievre','3ParvisDeLaBievre', [ 0 ], [ 28 ]))
cons_list.append(Consumer.Consumer('5ParvisDeLaBievre','5ParvisDeLaBievre', [ 0 ], [ 28 ]))
cons_list.append(Consumer.Consumer('PtiteEchoppe','PtiteEchoppe',[ 0 ], [ 27 ]))
cons_list.append(Consumer.Consumer('Azimut','Azimut',[ 0 ], [ 3 ]))

# cons_list[0].read_consumption('Simulation_AntonySoleil\\Simu_5Conso.csv')
# cons_list[1].read_consumption('Simulation_AntonySoleil\\Simu_Azimut.csv')
# cons_list[2].read_consumption('Simulation_AntonySoleil\\Simu_Harmony2.csv')
# cons_list[3].read_consumption('Simulation_AntonySoleil\\Simu_HautDeBievreHabitat12.csv')
# cons_list[4].read_consumption('Simulation_AntonySoleil\\Simu_HautDeBievreHabitat3.csv')
# cons_list[5].read_consumption('Simulation_AntonySoleil\\Simu_PtiteEchoppe.csv')

# cons_list[0].read_consumption('Releve_AntonySoleil\\Parking_Harmony2_Conso_202312_202412_V4.csv')
cons_list[0].read_consumption('Releve_AntonySoleil\\Simu_5Conso.csv')
cons_list[1].read_consumption('Releve_AntonySoleil\\1_1ParvisDuBreuil_PRM_30002130432283_V2.csv')
cons_list[2].read_consumption('Releve_AntonySoleil\\2_2ParvisDuBreuil_PRM_30002130432722_V2.csv')
cons_list[3].read_consumption('Releve_AntonySoleil\\3_3ParvisDuBreuil_PRM_30002130426648_V2.csv')
cons_list[4].read_consumption('Releve_AntonySoleil\\1_1ParvisDuBreuil_PRM_30002130432283_V2.csv')
cons_list[5].read_consumption('Releve_AntonySoleil\\2_2ParvisDuBreuil_PRM_30002130432722_V2.csv')
cons_list[6].read_consumption('Releve_AntonySoleil\\3_3ParvisDuBreuil_PRM_30002130426648_V2.csv')
cons_list[7].read_consumption('Releve_AntonySoleil\\Simu_PtiteEchoppe.csv')
cons_list[8].read_consumption('Releve_AntonySoleil\\Simu_Azimut.csv')

# Calculate repartition keys
rep = Repartition.Repartition('Novembre')
rep.build_rep(prod_list, cons_list)

rep.write_repartition_key(prod_list, cons_list)

rep.generate_statistics(prod_list, cons_list)

rep.generate_monthly_report(prod_list, cons_list)

auto_consumption_rate = rep.get_auto_consumption_rate(0)
print("Taux d'autoconsommation : ",auto_consumption_rate,"%")

index_cons = 0
auto_production_rate_global = 0
for cons in cons_list:
    auto_production_rate = rep.get_auto_production_rate(index_cons)
    auto_production_rate_global += auto_production_rate
    # print("Taux d'autoproduction de",cons.name,": ", auto_production_rate, "%")
    index_cons += 1
auto_production_rate_global = rep.get_global_auto_production_rate(cons_list)
print("Taux d'autoproduction global : ", auto_production_rate_global, "%")

coverage_rate = rep.get_coverage_rate(0, cons_list)
print("Taux de couverture : ",coverage_rate,"%")