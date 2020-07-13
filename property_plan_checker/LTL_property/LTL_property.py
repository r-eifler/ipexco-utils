from general.property import PlanProperty
from action_sets.action import ActionSet
from logic.logic_formula import *


class LTLProperty(PlanProperty):

    def __init__(self, name, formula, constants):
        super().__init__(name, formula)
        self.constants = constants
        
    def SAS_repr(self, actionSets):
        return self.name, self.formula.SAS_repr(actionSets)

    @staticmethod
    def fromJSON(json, typeObjectMap):
        (formula, rest, constants) = parseFormula(json['formula'])
        new_property = LTLProperty(json['name'], formula, constants)
        for actionSets_json in json['actionSets']:
            new_property.add_action_set(ActionSet.fromJSON(actionSets_json, typeObjectMap, True))
        return new_property

    def buildEnvironment(self, plan):
        for i, step in enumerate(plan.states):
            for action_set in self.actionSets:
                for action in step:
                    if action_set.containsAction(action):
                        plan.satActionSets[i].append(action_set.name)
                        break

    def check(self, plan):
        self.buildEnvironment(plan)
        return self.formula.evalLTL(plan)

    def __repr__(self):
        s = self.name + ":\n\t" + str(self.formula)
        return s


def removeDuplicates(list):
    new_list = []
    for e in list:
        if e in new_list:
            continue
        new_list.append(e)
    return new_list
