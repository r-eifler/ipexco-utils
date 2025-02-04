from general.property import PlanProperty


class GoalProperty(PlanProperty):

    def __init__(self, id, name, formula):
        super().__init__(id, name, formula)


    @staticmethod
    def fromJSON(json, typeObjectMap):
        formula = json['formula']
        new_property = GoalProperty(json['_id'], json['name'], formula)
        return new_property

    def check(self, states):
        lastState = states.last_elem()
        return self.formula in lastState

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
