import os

#Run FD
prefix = ""

VAL_temp = prefix + "VAL_temp"

VAL = os.environ['VAL'] + "validate -v"
# VAL = "/./home/eifler/XPP/framework/property_plan_checker/validate -v "
python = "python3"

fuel_predicates = ["energy", "fuel", "money"]
static_predicates = ["sum", "ecost", "connected", "fuelcost", "price", "drive-cost", "visible", "energycost", "can_traverse", "visible_from"]

ignore_predicates = fuel_predicates + static_predicates