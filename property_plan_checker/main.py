#! /usr/bin/env python3

from general.plan import Plan, PlanParser
from general import ExplanationSetting
from parser import parse
import json

import sys

def run(domain_path, problem_path, properties_path, task_schema_path, plan_path, print_res=False):
	EXPSET = ExplanationSetting()

	typeObjectMap = {}
	json_task_schema = json.load(open(task_schema_path))
	for o in json_task_schema['objects']:
		if not o['type'] in typeObjectMap:
			typeObjectMap[o['type']] = []

		typeObjectMap[o['type']].append(o['name'])

	# print("Schema parsed ...")

	# for properties_path in properties_paths:
	parse(properties_path, typeObjectMap, EXPSET)

	# print("Properties parsed ...")
	# print("#ASP: " + str(len(EXPSET.action_set_properties)))
	# print("#LTLP: " + str(len(EXPSET.ltl_properties)))

	planParser = PlanParser(domain_path, problem_path, plan_path, json_task_schema)
	actions, states = planParser.run()
	# print("Plan length: " + str(len(actions)))
	if not actions or not states:
		return None
	# plan.print()
	# print("--------------------------------------------------")
	# print("Properties parsed ...")
	# print("#Steps: " + str(len(plan.steps)))

	sat_props = []

	for prop in EXPSET.get_action_set_properties():
		sat = prop.check(actions)
		if sat:
			if print_res:
				print(prop.name)
			sat_props.append(prop.name)

	for prop in EXPSET.get_ltl_properties():
		# print(prop)
		if prop.vars_only_action_sets():
			sat = prop.checkPlan(actions)
		else:
			if prop.vars_only_facts():
				sat = prop.checkStates(states)
			else:
				assert False, 'You cannot used facts and action sets in the same planProperty'
		if sat:
			if print_res:
				print(prop.name)
			sat_props.append(prop.name)

	for prop in EXPSET.get_goal_properties():
		sat = prop.check(states)
		if sat:
			if print_res:
				print(prop.name)
			sat_props.append(prop.name)

	return sat_props


if __name__ == "__main__":
	domain_path = sys.argv[1]
	problem_path = sys.argv[2]
	properties_path = sys.argv[3]
	task_schema_path = sys.argv[4]
	plan_path = sys.argv[5]

	run(domain_path, problem_path, properties_path, task_schema_path, plan_path, print_res=True)
