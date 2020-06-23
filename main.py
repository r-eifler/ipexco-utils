import os
import json
import sys

from check_plans import check_plan_properties
from compute_MUGS import compute_mugs
from compute_plans import compute_plans
from plan_properties import PlanProperties
from settings import FD


def propsPlanToJSON(item):
    s = "{\n"
    s += "\"planProperties\": ["
    s += ", ".join(["\"" + p + "\"" for p in item[0]])
    s += "],\n\"plan\": \"" + item[1].split("/")[-1] + "\""
    s += "\n}"
    return s


def toJSON(MUGS, plans, sat_props_per_plan, stream):
    print("{\n\"MUGS\":", file=stream)
    print(MUGS.toJSON() + ",", file=stream)

    print("\"plans\": [", file=stream)
    print(",\n".join([propsPlanToJSON(item) for item in plans]), file=stream)
    print("]\n,", file=stream)

    print("\"satPropertiesPerPlan\":[", file=stream)
    print(",\n".join(propsPlanToJSON(item) for item in sat_props_per_plan), file=stream)
    print("]\n", file=stream)

    print("}", file=stream)


def run(run_folder, domain_path, problem_path, task_schema_path, plan_properties_path, result_folder):

    # create run environment
    # print("Runfolder: " + run_folder)
    os.system("mkdir -p " + run_folder)
    os.system("cp " + domain_path + " " + run_folder + "/domain.pddl" )
    os.system("cp " + problem_path + " " + run_folder + "/problem.pddl")
    # os.system("cp -r " + FD + " " + run_folder + "/fast-downward")
    # print("run environment created")

    task_schema = json.load(open(task_schema_path))
    # print("Task loaded ...")

    planProperties = PlanProperties(plan_properties_path)
    # print("Properties loaded ...")

    MUGS = compute_mugs(run_folder, task_schema, planProperties)
    # print("MUGS computed ...")

    plans = compute_plans(run_folder, task_schema, planProperties, MUGS, result_folder)
    # print("Plans computed ...")

    sat_props_per_plan = check_plan_properties(run_folder, plans, MUGS, planProperties, task_schema_path)
    # print("sat_props_per_plan computed ...")

    toJSON(MUGS, plans, sat_props_per_plan, sys.stdout)

run_folder = sys.argv[1]
domain_path = sys.argv[2]
problem_path = sys.argv[3]
task_schema_path = sys.argv[4]
plan_properties_path = sys.argv[5]
result_folder = sys.argv[6]

run(run_folder, domain_path, problem_path, task_schema_path, plan_properties_path, result_folder)