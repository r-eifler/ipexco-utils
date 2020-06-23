import os
import os.path

from exp_setting import ExplanationSetting
from settings import args_optimal_call, FD


def compute_plans(run_folder, task_schema, properties, MUGS, result_folder):
    plans = []
    all_property_names = [p['name'] for p in properties];
    solvable_subsets = MUGS.get_solvable_subsets(all_property_names)
    # print("Solvable Subset: ")
    # print(len(solvable_subsets))

    for sss_names in solvable_subsets:
        sss_properties = list(filter(lambda x: x['name'] in sss_names, properties))
        id = get_pp_set_id(sss_properties)
        result_path = "/".join([result_folder, "plan_" + id + ".sas"])

        hardGoals = task_schema['goal'] + [p['name'] for p in sss_properties]
        # print(hardGoals)
        exp_setting = ExplanationSetting(
            sss_properties,
            hardGoals,
            []
        )
        assert call_FD(run_folder, exp_setting, result_path), "No plan found!"
        plans.append((sss_names, result_path))
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
        FD,
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
