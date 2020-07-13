import json

from AS_property.action_set_property import ActionSetProperty
from G_property.goal_property import GoalProperty
from LTL_property.LTL_property import LTLProperty

# typeObjectMap maps from a type to a list of objects which have this type
def parse(path, typeObjectMap, EXPSET):

    with open(path, encoding='utf-8') as fh:
        json_encoding = json.load(fh)

    for p_json in json_encoding["plan_properties"]:
        if p_json['type'] == 'AS':
            property = ActionSetProperty.fromJSON(p_json, typeObjectMap)
            EXPSET.add_action_set_property(property)
        elif p_json['type'] == 'LTL':
            property = LTLProperty.fromJSON(p_json, typeObjectMap)
            EXPSET.add_ltl_property(property)
        elif p_json['type'] == 'G':
            property = GoalProperty.fromJSON(p_json, typeObjectMap)
            EXPSET.add_goal_property(property)
        else:
            assert False, "Unknown property type: " + p_json['type']
        for set in property.get_action_sets():
            EXPSET.add_action_set(set)

