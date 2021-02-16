import json


class PlanProperties(list):

    def __init__(self, plan_properties_path):
        super().__init__()
        file = open(plan_properties_path)
        jsonObject = json.load(file)
        file.close()
        for p in jsonObject:
            self.append(p)
