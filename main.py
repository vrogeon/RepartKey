import logging
from logging import basicConfig
import math
import Consumer
import Producer
import Repartition

# Idea 1: Use recursive function to optimize consumption from producers
# Idea 2: Use priority 0, 1 ,2... to define consumers that have priority (it can be per producers)
# Idea 3: Update float representation of repartition key to limit lost of production

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


###################### Start of program ######################

# Define variable to select projects an installator
#project = "Test"
project = "Val_De_Bievre"
# project = "Grand_Cedre"

#installator = "Simu"
installator = "Enerev_100"
#installator = "Enerev_75"
# installator = "Soli_100"
# installator = "Soli_75"

# Define strategy to use for key computation
strategy = Repartition.Strategy.DYNAMIC_BY_DEFAULT

# Initialize list of producer and consumer
prod_list = []
cons_list = []

# Select producers and consumers according project selected
if project == "Test":
    prod_list.append(Producer.Producer('Prod1', 1234567901000,'Courbe_charge_producteur1.txt'))
    prod_list.append(Producer.Producer('Prod2', 1234567901099,'Courbe_charge_producteur2.txt'))

    cons_list.append(Consumer.Consumer('Cons1', 12345678900001, [ 0 , 2 ], [ 50 , 10 ],'Courbe_charge_consommateur1.txt'))
    cons_list.append(Consumer.Consumer('Cons1', 12345678900002, [ 2 , 0 ], [ 20 , 50 ],'Courbe_charge_consommateur2.txt'))
    cons_list.append(Consumer.Consumer('Cons1', 12345678900003, [ 1 , 0 ], [ 30 , 20 ],'Courbe_charge_consommateur3.txt'))

elif project == "Val_De_Bievre":

    if installator ==  "Simu":
        prod_list.append(Producer.Producer('Prod1', 1234567901000, 'Simulation_AntonySoleil\\Simu_Prod.csv'))
    if installator == "Enerev_100":
        prod_list.append(Producer.Producer('Prod1', 1234567901000, 'Releve_AntonySoleil\\Simu_Prod_Enerev_100.csv'))
    elif installator == "Enerev":
            prod_list.append(Producer.Producer('Prod1', 1234567901000, 'Releve_AntonySoleil\\Simu_Prod_Enerev.csv'))
    elif installator == "Soli_100":
        prod_list.append(Producer.Producer('Prod1', 1234567901000, 'Releve_AntonySoleil\\Simu_Prod_Soli_100.csv'))
    elif installator == "Soli_75":
        prod_list.append(Producer.Producer('Prod1', 1234567901000, 'Releve_AntonySoleil\\Simu_Prod_Soli_75.csv'))
    else:
        print("No installator selected")

    cons_list.append(Consumer.Consumer('Parking_Harmony1','Parking_Harmony1',[ 0 ], [ 50 ], 'Releve_AntonySoleil\\Parking_Harmony1_Conso_202312_202412_V1.csv'))
    cons_list.append(Consumer.Consumer('Parking_Harmony2','Parking_Harmony2',[ 0 ], [ 50 ], 'Releve_AntonySoleil\\Parking_Harmony2_Conso_202312_202412_V5.csv'))
    cons_list.append(Consumer.Consumer('Particuliers', 'Particuliers', [1], [100], 'Releve_AntonySoleil\\Simu_50_particuliers.csv'))
    cons_list.append(Consumer.Consumer('1ParvisDuBreuil', '1ParvisDuBreuil', [3], [16], 'Releve_AntonySoleil\\1_1ParvisDuBreuil_PRM_30002130432283_V2.csv'))
    cons_list.append(Consumer.Consumer('2ParvisDuBreuil', '2ParvisDuBreuil', [3], [16], 'Releve_AntonySoleil\\2_2ParvisDuBreuil_PRM_30002130432722_V2.csv'))
    cons_list.append(Consumer.Consumer('3ParvisDuBreuil', '3ParvisDuBreuil', [3], [16], 'Releve_AntonySoleil\\3_3ParvisDuBreuil_PRM_30002130426648_V2.csv'))
    cons_list.append(Consumer.Consumer('2ParvisDeLaBievre', '2ParvisDeLaBievre', [3], [16], 'Releve_AntonySoleil\\1_1ParvisDuBreuil_PRM_30002130432283_V2.csv'))
    cons_list.append(Consumer.Consumer('3ParvisDeLaBievre', '3ParvisDeLaBievre', [3], [16], 'Releve_AntonySoleil\\2_2ParvisDuBreuil_PRM_30002130432722_V2.csv'))
    cons_list.append(Consumer.Consumer('5ParvisDeLaBievre', '5ParvisDeLaBievre', [3], [16], 'Releve_AntonySoleil\\3_3ParvisDuBreuil_PRM_30002130426648_V2.csv'))
    cons_list.append(Consumer.Consumer('PtiteEchoppe', 'PtiteEchoppe', [2], [50], 'Releve_AntonySoleil\\Simu_PtiteEchoppe.csv'))
    cons_list.append(Consumer.Consumer('Azimut', 'Azimut', [2], [50], 'Releve_AntonySoleil\\Simu_Azimut.csv'))

elif project == "Grand_Cedre":
    prod_list.append(Producer.Producer('Prod1', 30002132191769, file='Grand_cedre\\Simu_Prod_Grand_cedre.csv'))
    prod_list[0].apply_factor(0.9)
    cons_list.append(Consumer.Consumer('Grand_cedre', 'Grand_cedre', [0], [100],'Grand_cedre\\Conso_2022_30002132191769_2.csv'))

else:
    print("No project selected")


# Calculate repartition keys
rep = Repartition.Repartition('Novembre')
rep.build_rep(prod_list, cons_list, strategy)

rep.write_repartition_key(prod_list, cons_list, True)

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