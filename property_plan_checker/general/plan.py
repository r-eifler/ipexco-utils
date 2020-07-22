from typing import List

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
                plan.add_action(action_line)

        fileIn.close()

        # write plan file with only original actions for VAL
        fileOut = open(self.plan_path, 'wt')
        fileOut.writelines(original_task_actions)
        fileOut.close()

        # get facts from VAL
        # print("Get facts from VAL")
        valConnection = VALConnection(self.domain, self.problem)
        valConnection.add_states(self.plan_path, plan)

        return plan


class Plan:

    def __init__(self):
        self.actions = []
        self.states = []
        self.satActionSets = []

    def print(self):
        print("*********************")
        for a in self.actions:
            print(a)
        print("*********************")
        for s in self.states:
            print(s)
        print("*********************")

    def add_action(self, action):
        self.actions.append(action)
        # self.states.append([])
        self.satActionSets.append([])
        assert len(self.actions) == len(self.satActionSets), str(len(self.actions)) + " != " + str(len(self.satActionSets))

    def next_step(self):
        return self.states[0]

    def head(self):
        assert(len(self.states) > 1 and len(self.satActionSets) > 1)
        newPlan = Plan()
        newPlan.actions = self.actions[0]
        newPlan.states = self.states[0]
        newPlan.satActionSets = self.satActionSets[0]
        return newPlan

    def tail(self):
        newPlan = Plan()
        newPlan.actions = self.actions[1:]
        newPlan.states = self.states[1:]
        newPlan.satActionSets = self.satActionSets[1:]
        return newPlan

    def last(self):
        newPlan = Plan()
        newPlan.actions = self.actions[-1]
        newPlan.states = self.states[-1]
        newPlan.satActionSets = self.satActionSets[-1]
        return newPlan

    def __len__(self):
        return len(self.states)


