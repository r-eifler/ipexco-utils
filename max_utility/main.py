import sys

from plan_properties import PlanProperties
from MUGS import MUGS
from linear_programm import LinearProgram

def run(plan_properties_path, MUGS_path):

    plan_properties = PlanProperties(plan_properties_path)

    vars = []
    utilities = []
    for pp in plan_properties:
        #if not pp['globalHardGoal']:
        vars.append(pp['name'])
        utilities.append(pp['value'])

    constraints = MUGS(plan_properties, MUGS_path)

    if len(constraints) == 0:
        max_utility = 0
        for i, r in enumerate(plan_properties):
            max_utility += utilities[i]

        print('{')
        #print('\"selectedPlanProperties\": [' + ','.join(['\"' + pp + '\"' for pp in plan_properties]) + '],')
        print('\"value\": ' + str(max_utility))
        print('}')
        return


    # print(vars)
    # print(utilities)
    # print(constraints)

    # print("Num vars: " + str(len(vars)))
    # print("Num constraints: " + str(len(constraints)))

    linProg = LinearProgram(vars, utilities, constraints)
    used_pp = linProg.compute()

    max_utility = 0
    selected_PP = []
    for i, r in enumerate(used_pp):
        if r > 0:
            # print(vars[i])
            selected_PP.append(vars[i])
            max_utility += utilities[i]

    selected_PP.sort()

    print('{')
    print('\"selectedPlanProperties\": [' + ','.join(['\"' + pp + '\"' for pp in selected_PP]) + '],')
    print('\"value\": ' + str(max_utility))
    print('}')


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])


