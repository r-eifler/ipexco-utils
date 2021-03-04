import os

args_optimal_call = ['--search', '\"astar(lmcut())\"']
args_mugs_call = ['--heuristic', 'h=\"hc(nogoods=false, cache_estimates=false)\"', '--heuristic',
   'mugs_h=\"mugs_hc(hc=h, all_softgoals=false)\"', '--search', '\"dfs(u_eval=mugs_h)\"']

#args_mugs_call = ["--heuristic", "hp=\"iPDB()\"",
 #   "--search", "\"goal_relation([lazy_greedy([hp], reopen_closed=true)], heu=[hp], metasearch=bottomupmugssearch)\""]

# --heuristic h="hc(nogoods=false, cache_estimates=false)" --heuristic mugs_h="mugs_hc(hc=h, all_softgoals=false)" --search "dfs(u_eval=mugs_h)"

# FD = "/home/eifler/XPP/framework/fast-downward/run_FD.py"
# FD_script_name = "run_FD.py"
# property_checker = "/home/eifler/XPP/framework/property_plan_checker/main.py"


FD = os.environ['PLANNER']
FD_script_name = "run_FD.py"
property_checker = os.environ['PROPERTYCHECKER']