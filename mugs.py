import itertools


class MUGS:

    def __init__(self, mugsJSON):
        self.goal_exclusion_sets = []
        json_dict = mugsJSON['MUGS']
        for m in json_dict:
            mugs = []
            for f in m:
                f = f.replace("sat_", '')
                mugs.append(f)
            self.goal_exclusion_sets.append(mugs)

    def toJSON(self):
        s = "[\n"
        parts = []
        for ms in self.goal_exclusion_sets:
            parts.append(", ".join(["\"" + str(elem) + "\"" for elem in ms]))
        s += ",\n".join(["\t[" + s + "]" for s in parts])
        s += "\n]"
        return s

    def get_solvable_subsets(self, all_facts):
        all_facts_set = set(all_facts)
        for ge in self.goal_exclusion_sets:
            all_facts_set = all_facts_set.difference(set(ge))
        always_solvable = list(all_facts_set)

        solvable_sets = set()
        for ge in self.goal_exclusion_sets:
            # print(ge)
            for i in range(1,len(ge)):
                subsets = set(itertools.combinations(ge + always_solvable, i))
                solvable_sets = solvable_sets.union(subsets)
        return list(solvable_sets)

    def get_contradicting_goal_facts(self, facts):
        facts = set()
        for f in facts:
            for mugs in self.goal_exclusion_sets:
                if f in mugs:
                    facts.add(mugs)
            facts.remove(f)
        return facts



