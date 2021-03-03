from mip import *


class LinearProgram:

    def __init__(self, vars, utilities, constraints):
        self.vars = vars
        self.utilities = utilities
        self.constraints = constraints

    def compute(self):

        m = Model(sense=MAXIMIZE, solver_name=CBC)
        m.verbose = False

        variables = [m.add_var(name=v, var_type=BINARY) for v in self.vars]

        for c in self.constraints:
            m += xsum(variables[i] for i, v in enumerate(self.vars) if v in c) <= (len(c) - 1)

        m.objective = maximize(xsum(self.utilities[i] * variables[i] for i, v in enumerate(self.vars)))

        res = []
        m.max_gap = 0.05
        status = m.optimize(max_seconds=300)
        # if status == OptimizationStatus.OPTIMAL:
        #     print('optimal solution cost {} found'.format(m.objective_value))
        # elif status == OptimizationStatus.FEASIBLE:
        #     print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
        # elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        #     print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
        if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
            # print('solution:')
            for v in m.vars:
                if abs(v.x) > 1e-6:  # only printing non-zeros
                    # print('{} : {}'.format(v.name, v.x))
                    res.append(v.name)

        return res
