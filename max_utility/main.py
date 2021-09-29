import sys

from plan_properties import PlanProperties
from MUGS import MUGS
from mixed_integer_linear_programm import LinearProgram

def run(plan_properties_path, MUGS_path):

    plan_properties = PlanProperties(plan_properties_path)

    vars = []
    utilities = []
    utility_map = {}
    hard_goals_utility = 0
    hard_goals = []
    for pp in plan_properties:
        #if not pp['globalHardGoal']:
        vars.append(pp['name'])
        utilities.append(pp['value'])
        utility_map[pp['name']] = pp['value']
        # else:
        #     hard_goals.append(pp)
        #     hard_goals_utility += pp['value']

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
    #print(constraints)

    # print("Num vars: " + str(len(vars)))
    # print("Num constraints: " + str(len(constraints)))

    linProg = LinearProgram(vars, utilities, constraints)
    selected_PP = linProg.compute()

    max_utility = sum(utility_map[p] for p in selected_PP)
    #max_utility += hard_goals_utility
    #selected_PP += hard_goals

    # for p, u in zip(vars, utilities):
    #     if p in selected_PP:
    #         print('1: ' + p + ' ' + str(u))
    #     else:
    #         print('0: ' + p + ' ' + str(u))

    # pip3 install mip

    print('{')
    print('\"selectedPlanProperties\": [' + ','.join(['\"' + pp + '\"' for pp in selected_PP]) + '],')
    print('\"value\": ' + str(max_utility))
    print('}')


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])


