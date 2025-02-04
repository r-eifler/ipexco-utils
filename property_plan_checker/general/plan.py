from typing import List
import json

from VAL.val_connection import VALConnection


class PlanParser:

    def __init__(self, domain, problem, plan_path, task_schema):
        self.domain = domain
        self.problem = problem
        self.plan_path = plan_path
        self.original_task_actions_names = [a['name'] for a in task_schema['actions']]

    def run(self):
        original_task_actions = []

        # parse actions
        
        with open(self.plan_path) as fp:
            actions = json.load(fp)

        plan = Plan()
        for a in actions:
            plan.add(a)
            original_task_actions.append( '(' + a['name'] + ' ' + ' '.join(a['params']) + ')\n')

        self.sas_plan_path = self.plan_path.replace('.json', '_sas')

        # write plan file with only original actions for VAL
        fileOut = open(self.sas_plan_path, 'wt')
        fileOut.writelines(original_task_actions)
        fileOut.close()

        # get facts from VAL
        # print("Get facts from VAL")
        states = Plan()
        valConnection = VALConnection(self.domain, self.problem)
        valConnection.add_states(self.sas_plan_path, states)

        return plan, states


class Plan:

    def __init__(self):
        self.elems = []

    def print(self):
        print("*********************")
        for a in self.elems:
            print(a)
        print("*********************")

    def add(self, elem):
        self.elems.append(elem)

    def __copy__(self):
        newPlan = Plan()
        newPlan.elems = self.elems.copy()

    def first_elem(self):
        return self.elems[0]

    def head(self):
        assert (len(self.elems) >= 1)
        newPlan = Plan()
        newPlan.elems = [self.elems[0]]
        return newPlan

    def tail(self):
        newPlan = Plan()
        newPlan.elems = self.elems[1:]
        return newPlan

    def last_elem(self):
        return self.elems[-1]

    def __len__(self):
        return len(self.elems)


