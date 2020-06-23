import os
import json

from exp_setting import ExplanationSetting
from mugs import MUGS
from settings import args_mugs_call, FD


def compute_mugs(run_folder, task_schema, properties):

    exp_setting = ExplanationSetting(properties, task_schema['goal'], [p['name'] for p in properties])
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
        FD,
        run_folder,
        "--build", "release64",
        "/".join([run_folder, "domain.pddl"]),
        "/".join([run_folder, "problem.pddl"]),
        "/".join([run_folder, "exp_setting.pddl"]),
        " ".join(args_mugs_call),
        " > /dev/null"])
    # print(cmd)
    os.system(cmd)

