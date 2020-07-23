from logic.logic_formula import *
from general.property import PlanProperty
from action_sets.action import ActionSet


class ActionSetProperty(PlanProperty):

    def __init__(self, name, formula, constants=[]):
        super().__init__(name, formula)
        # names of the set names that are used in the property
        self.constants = constants

    # used to generate one instance of the property in a propertylass
    def generateInstance(self, instance_postfix):
        formula_instance = self.formula.addPostfix(instance_postfix)
        instance_constants = []
        for c in self.constants:
            instance_constants.append(c +instance_postfix)

        return ActionSetProperty(self.name + instance_postfix, formula_instance, instance_constants)

    def containsSet(self, set_name):
        return set_name in self.constants 

    def getClauses(self):
        if(isinstance(self.formula, LOr)): #TODO
            return self.formula.getClauses([])
        else:
            return [self.formula.getClauses([])]

    def get_negated_Clauses(self):
        neg_formula = self.formula.negate()
        DNF_neg_formula = neg_formula.toDNF()
        if(isinstance(DNF_neg_formula, LOr)): #TODO
            return DNF_neg_formula.getClauses([])
        else:
            return [DNF_neg_formula.getClauses([])]

    @staticmethod
    def fromJSON(json, typeObjectMap):
        (formula, rest, constants) = parseFormula(json['formula'])
        new_property = ActionSetProperty(json['name'], formula, constants)
        for actionSets_json in json['actionSets']:
            new_property.add_action_set(ActionSet.fromJSON(actionSets_json, typeObjectMap, False))
        return new_property

    def buildEnvironment(self, plan):
        env = []
        for action_set in self.actionSets:
            for action in plan.elems:
                if action_set.containsAction(action):
                    env.append(action_set.name)
                    break
        return env

    def check(self, plan):
        env = self.buildEnvironment(plan)
        return self.formula.evalAS(env)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
