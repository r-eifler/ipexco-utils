import json

class ExplanationSetting:

    def __init__(self, properties, hardGoals, softGoals):
        self.properties = properties
        self.hardGoals = hardGoals
        self.softGoals = softGoals

    def toJSON(self, outStream):
        print("{", file=outStream)

        print("\"plan_properties\": [", file=outStream)
        print(", ".join([json.dumps(p) for p in self.properties]), file=outStream)
        print("\n],", file=outStream)

        print("\"hard_goals\": [", file=outStream)
        print(", ".join(["\"" + g + "\"" for g in self.hardGoals]), file=outStream)
        print("],\n", file=outStream)

        print("\"soft_goals\": [", file=outStream)
        print(", ".join(["\"" + g + "\"" for g in self.softGoals]), file=outStream)
        print("]\n", file=outStream)

        print("}", file=outStream)
