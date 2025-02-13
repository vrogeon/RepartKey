import Consumer

# Production in kW
prod = 10

keys = { 'partA': Consumer.Consumer('partA',0.5, 4),
         'partB': Consumer.Consumer('partB',0.2, 5),
         'partC': Consumer.Consumer('partC',0.3, 5)
         }

# Function to compute auto consumption
def cal_cons(prod):
    # Production used
    prod_used = 0

    # First iterates on all consumers to assign consumption according ratio
    for part, cons in keys.items():
        # Manage only active consumers
        if cons.active:
            if cons.cons < prod * cons.ratio:
                cons.colcons += cons.cons
                cons.active = False
            else:
                cons.colcons += prod * cons.ratio

            prod_used += cons.colcons
            print("Consommation de",part, "est égale à",cons.colcons)

    # If not all the production is used, compute new ratios
    # and recursively call this function
    if prod_used < prod:
        # New sum to add ratios of all active consumers
        new_sum = 0
        for part, cons in keys.items():
            # Manage only active consumers
            if cons.active:
                new_sum += cons.ratio

        # Compute new ratios
        for part, cons in keys.items():
            # Manage only active consumers
            if cons.active:
                cons.ratio = cons.ratio / new_sum

        # Call again the function
        cal_cons(prod - prod_used)

cal_cons(prod)