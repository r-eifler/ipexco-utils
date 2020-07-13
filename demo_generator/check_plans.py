import os
import subprocess

from exp_setting import ExplanationSetting
from settings import property_checker


def check_plan_properties(run_folder, plans, MUGS, properties, task_schema_path):
    # print(plans)
    sat_props_per_plan = []
    for sss, plan_path in plans:
        not_satisfiable_props = MUGS.get_contradicting_goal_facts(sss)

        possible_satisfiable_props = set([p['name'] for p in properties]).difference(sss).difference(not_satisfiable_props)
        exp_setting = ExplanationSetting([p for p in properties if p['name'] in possible_satisfiable_props], [], [])
        additional_satisfiable_props = call_Checker(run_folder, exp_setting, task_schema_path, plan_path)

        sat_props_per_plan.append((list(set(additional_satisfiable_props).union(sss)), plan_path))
    return sat_props_per_plan



def call_Checker(run_folder, exp_setting, task_schema_path, plan_path):
    if len(exp_setting.properties) == 0:
        return []
    exp_setting.toJSON(open("/".join([run_folder, "exp_setting.pddl"]), 'w'))
    cmd = " ".join([
        property_checker,
        "/".join([run_folder, "domain.pddl"]),
        "/".join([run_folder, "problem.pddl"]),
        "/".join([run_folder, "exp_setting.pddl"]),
        task_schema_path,
        plan_path
    ])
    # print(cmd)
    result = subprocess.check_output(cmd, shell=True)
    return list(filter(lambda  x: x != '', result.decode('utf-8').split("\n")))