import json

def parseHardGoals(path):
    file = open(path)
    jsonObject = json.load(file)
    file.close()
    return jsonObject['hard_goals']
