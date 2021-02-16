import json

class MUGS(list):

    def __init__(self, plan_properties, path):
        super().__init__()
        temp = []
        file = open(path)
        jsonObject = json.load(file)
        file.close()
        for m in jsonObject['MUGS']:
            temp.append(m)

        for mugs in temp:
            renamed = []
            goal_pp = [pp for pp in plan_properties if pp['type'] == 'G']
            for v in mugs:
                if not v.startswith('Atom'):
                    renamed.append(v.replace('soft_accepting(','').replace(')',''))
                    continue

                pred = v.replace('Atom ','').replace(' ','')
                for pp in goal_pp:
                    if pp['formula'] == pred:
                        renamed.append(pp['name'])
                        break

            self.append(renamed)
