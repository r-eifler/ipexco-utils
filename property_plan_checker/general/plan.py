from typing import List

from  ..VAL.val_connection import VALConnection


class PlanParser:

    def __init__(self, domain, problem, plan_path, task_schema):
        self.domain = domain
        self.problem = problem
        self.plan_path = plan_path
        self.original_task_actions_names = [a['name'] for a in task_schema['actions']]

    def run(self):
        original_task_actions = []

        # parse actions
        fileIn = open(self.plan_path, 'rt')
        plan = Plan()
        for line in fileIn.readlines():
            if line.startswith(";"):
                original_task_actions.append(line)  # action cost line
                break
            action_line = line.replace('(', '').replace(')', '').replace("\n", '')
            action_parts = action_line.split(' ')
            action_name =  action_parts[0]
            if action_name in self.original_task_actions_names:
                original_task_actions.append(line)
                plan.add(action_line)

        fileIn.close()

        # write plan file with only original actions for VAL
        fileOut = open(self.plan_path, 'wt')
        fileOut.writelines(original_task_actions)
        fileOut.close()

        # get facts from VAL
        # print("Get facts from VAL")
        states = Plan()
        valConnection = VALConnection(self.domain, self.problem)
        valConnection.add_states(self.plan_path, states)

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


