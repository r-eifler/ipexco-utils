import os
import os.path

from exp_setting import ExplanationSetting
from settings import args_optimal_call, FD, FD_script_name


def compute_plans(run_folder, task_schema, properties, MUGS, result_folder):
    plans = []
    all_property_names = [p['name'] for p in properties];
    solvable_subsets = MUGS.get_solvable_subsets(all_property_names)
    # all solvable subsets with goal facts
    # solvable_subsets = MUGS.get_solvable_subsets(all_property_names + task_schema['goal'])
    # print("Solvable Subset: ")
    # print(len(solvable_subsets))
    if len(solvable_subsets) > 1000:
        return []

    num_plans = 0
    for sss_names in solvable_subsets:
        # if num_plans % 10 == 0:
        #     print(str(num_plans) + "/" + str(len(solvable_subsets)))
        solvablesubsets_properties = list(filter(lambda x: x['name'] in sss_names, properties))
        id_properties = get_pp_set_id(solvablesubsets_properties)

        # solvablesubsets_goalfacts = list(filter(lambda x: x in sss_names, task_schema['goal']))
        # id_goalfacts = get_goal_set_id(solvablesubsets_goalfacts, task_schema['goal'])

        # result_path = "/".join([result_folder, "plan_" + id_properties + "-" + id_goalfacts + ".sas"])
        result_path = "/".join([result_folder, "plan_" + id_properties + ".sas"])

        # hardGoals = solvablesubsets_goalfacts + [p['name'] for p in solvablesubsets_properties]
        hardGoals = [p['name'] for p in solvablesubsets_properties]
        # print(hardGoals)
        exp_setting = ExplanationSetting(
            solvablesubsets_properties,
            hardGoals,
            []
        )
        assert call_FD(run_folder, exp_setting, result_path), "No plan found!"
        plans.append((sss_names, result_path))
        num_plans += 1
    return plans


def call_FD(run_folder, exp_setting, result_path):
    # print("call FD")
    plan_path = run_folder + "/sas_plan"
    # os.system("rm " + plan_path)

    exp_setting_path = "/".join([run_folder, "exp_setting.pddl"])
    os.system("echo > " + exp_setting_path)

    exp_setting_file = open(exp_setting_path, 'w')
    exp_setting.toJSON(exp_setting_file)
    exp_setting_file.close()

    cmd = " ".join([
        "python3",
        FD + "/" + FD_script_name,
        run_folder,
        "--build", "release64",
        "/".join([run_folder, "domain.pddl"]),
        "/".join([run_folder, "problem.pddl"]),
        "/".join([run_folder, "exp_setting.pddl"]),
        " ".join(args_optimal_call),
        " > /dev/null"])
    # print(cmd)
    os.system(cmd)

    if os.path.exists(plan_path):
        os.system("cp " + plan_path + " " + result_path)
        return True

    return False


def get_pp_set_id(s):
    l = list(s)
    l.sort(key=lambda x: x['id'])
    return ''.join([str(x['id']) for x in l])

def get_goal_set_id(id_set, all_goal_facts):
    all_goal_facts.sort()
    l = list(id_set)
    return ''.join([str(all_goal_facts.index(x)) for x in l])
