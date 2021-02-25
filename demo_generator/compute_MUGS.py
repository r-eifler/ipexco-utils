import os
import json

from exp_setting import ExplanationSetting
from mugs import MUGS
from settings import args_mugs_call, FD, FD_script_name


def compute_mugs(run_folder, task_schema, properties, global_hardgoals):

    soft_goals = [p['name'] for p in properties if p['name'] not in global_hardgoals]

    exp_setting = ExplanationSetting(properties, global_hardgoals, soft_goals)
    call_FD(run_folder, exp_setting)

    mugs_path = run_folder + "/mugs.json"
    mugsJSON = json.load(open(mugs_path))
    return MUGS(mugsJSON)


def call_FD(run_folder, exp_setting):
    # print("Call FD for MUGS computation ...")
    exp_setting_path = "/".join([run_folder, "exp_setting.pddl"])
    os.system("echo > " + exp_setting_path)

    exp_setting_file = open(exp_setting_path, 'w')
    exp_setting.toJSON(exp_setting_file)
    exp_setting_file.close()

    # print("Exp setting stored ...")

    cmd = " ".join([
        "python3",
        FD + "/" + FD_script_name,
        run_folder,
        "--build", "release64",
        "/".join([run_folder, "domain.pddl"]),
        "/".join([run_folder, "problem.pddl"]),
        "/".join([run_folder, "exp_setting.pddl"]),
        '--translate-options',
        '--keep-unreachable-facts',
        '--keep-unimportant-variables',
        '--search-options',
        " ".join(args_mugs_call),
        " > /dev/null"])
    os.system(cmd)

