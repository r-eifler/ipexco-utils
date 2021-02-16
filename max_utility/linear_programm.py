from scipy.optimize import linprog


class LinearProgram:

    def __init__(self, vars, utilities, constraints):
        self.vars = vars
        self.utilities = utilities
        self.constraints = constraints

    def compute(self):

        coefficients = [-v for v in self.utilities]

        bounds = [[0, 1] for v in self.vars]  # property either used or not

        A = []
        for c in self.constraints:
            f = []
            for v in self.vars:
                if v in c:
                    f.append(1)
                else:
                    f.append(0)
            A.append(f)

        b = [len(c) - 1 for c in self.constraints]

        # print('coefficients')
        # print(coefficients)
        # print('MUGS/Constraints')
        # print(A)
        # print("MUGS Size")
        # print(b)

        res = linprog(coefficients, A_ub=A, b_ub=b, bounds=bounds, method='revised simplex')
        # print(res)

        return res.x
