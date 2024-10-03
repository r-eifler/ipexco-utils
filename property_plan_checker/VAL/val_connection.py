from settings import VAL_temp, VAL, ignore_predicates
import os
import copy


class StateChange:

    def __init__(self):
        self.adds = []
        self.deletes = []


class VALConnection:

    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem

    def add_states(self, plan_path, plan):
        # print("Add states ...")
        initial_state = self.get_initial_state()

        state_changes, cost = self.get_state_changes(plan_path)
        if not state_changes:
            return 

        plan.add(initial_state)
        for change in state_changes:
            next_state = plan.elems[-1].copy()
            # print("Current state:")
            # print(next_state)
            # print("DELETE")
            # print(change.deletes)
            # print("ADD")
            # print(change.adds)
            for d in change.deletes:
                if d.split("(")[0] in ignore_predicates:
                    continue
                # assert d in next_state, "ERROR: " + d + " not in state: " + str(next_state)
                if d in next_state:
                    next_state.remove(d)
            for a in change.adds:
                if a.split("(")[0] in ignore_predicates:
                    continue
                next_state.append(a)

            #print(next_state)
            plan.add(next_state)

    def get_initial_state(self):

        problem_file = open(self.problem, "r")
        lines = problem_file.readlines()
        problem_file.close()

        line = lines.pop(0)
        while not line.startswith("(:init"):
            line = lines.pop(0)

        initial_state = []
        while len(lines) > 0:
            line = lines.pop(0).replace("\n", "")
            if line == "":
                continue
            if line.startswith("(:goal") or line == ")":
                break

            line = line.strip()
            fact_parts = line.replace("(", "").replace(")", "").split(" ")
            predicate = fact_parts[0]
            if predicate in ignore_predicates:
                continue
            initial_state.append(fact_parts[0] + "(" + ",".join(fact_parts[1:]) + ")")

        #print(initial_state)
        return initial_state

    def get_state_changes(self, plan_sas_file):

        cmd = VAL + " " + self.domain + " " + self.problem + " " + plan_sas_file + " > " + VAL_temp
        # print(cmd)
        os.system(cmd)

        # parse deletes and adds

        val_output = open(VAL_temp, "r")
        lines = val_output.readlines()
        val_output.close()

        state_changes = []
        cost = None
        assert len(lines) > 0, cmd
        line = lines.pop(0)
        while not line.startswith("-----------"):
            if len(lines) == 0:
                print(cmd)
                return None, None
            # assert len(lines) > 0, cmd
            line = lines.pop(0)

        while len(lines) > 0:
            line = lines.pop(0).replace("\n", "")
            if line.startswith("Checking next happening"):
                state_changes.append(StateChange())
                continue

            if line.startswith("Deleting"):
                fact_parts = line.replace("Deleting ", "").replace("(", "").replace(")", "").split(" ")
                state_changes[-1].deletes.append(fact_parts[0] + "(" + ",".join(fact_parts[1:]) + ")")
                continue

            if line.startswith("Adding"):
                fact_parts = line.replace("Adding ", "").replace("(", "").replace(")", "").split(" ")
                state_changes[-1].adds.append(fact_parts[0] + "(" + ",".join(fact_parts[1:]) + ")")
                continue

            #print(line)
            if line.startswith(("Final value:")):
                cost = int(line.split(" ")[-1])


        #print("Cost: " + str(cost))
        return state_changes, cost


