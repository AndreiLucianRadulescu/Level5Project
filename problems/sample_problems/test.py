from pulp import LpProblem
problem = LpProblem.from_lp_file("sample_basic.lp")
problem.solve()