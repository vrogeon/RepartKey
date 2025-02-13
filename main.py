import Consumer

# Production in kW
prod = 10
# Production used
prod_used = 0

keys = { 'partA': Consumer.Consumer('partA',0.5, 4),
         'partB': Consumer.Consumer('partB',0.2, 4),
         'partC': Consumer.Consumer('partC',0.3, 3)
         }

# Function to compute auto consumption
def cal_cons(prod, keys):
    # Use global variable
    global prod_used

    # First iterates on all consumers to assign consumption according ratio
    for part, cons in keys.items():
        # Manage only active consumers
        if cons.active:
            # Check if consumption from autocollect exceeds consumption
            if cons.cons < (cons.colcons + prod * cons.ratio):
                cons.colcons = cons.cons
                cons.active = False
            else:
                cons.colcons += prod * cons.ratio
            # print("Consommation de",part, "est égale à",cons.colcons)

            prod_used += cons.colcons
            # print("Production utilisée: ", prod_used)

    # If not all the production is used, compute new ratios
    # and recursively call this function
    if prod_used < prod:
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
        cal_cons(prod - prod_used, keys)

# Start of pogram
cal_cons(prod, keys)

# Print consumption from autocollective
for part, cons in keys.items():
    print("Consommation de", part, "est égale à", cons.colcons)