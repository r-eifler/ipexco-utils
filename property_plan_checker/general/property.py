
class PlanProperty:

    def __init__(self, id, name, formula):
        self._id = id
        self.name = name
        self.formula = formula
        self.actionSets = []
        # names of the set names that are used in the property
        self.constants = []
        # id of the sat variable in the SAS encoding
        self.var_id = None

    def vars_only_action_sets(self):
        for c in self.constants:
            if c not in [s.name for s in self.actionSets]:
                return False
        return True

    def vars_only_facts(self):
        for c in self.constants:
            if c in [s.name for s in self.actionSets]:
                return False
        return True



    def add_action_set(self, s):
        self.actionSets.append(s)

    def get_action_sets(self):
        return self.actionSets

    def add_constant(self, c):
        self.constants.append(c)

    def __repr__(self):
        s = self.name + ":\n"
        s += "\tformula:" + str(self.formula) + "\n"
        s += "\tvar_id:" + str(self.var_id)
        return s