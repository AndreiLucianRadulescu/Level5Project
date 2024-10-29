from input_parser import LPParser
from simplex_solver import SimplexSolver

lp_parser = LPParser()
# print(lp_parser)
lp_parser.parse_file("./problems/sample.lp")
# print(lp_parser)

solver = SimplexSolver(pivot_rule="Dantzig")

solver.solve(lp_parser)