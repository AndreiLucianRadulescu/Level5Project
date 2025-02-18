import sys
from input_parser import LPParser
from simplex_solver import SimplexSolver

lp_parser = LPParser()
# print(lp_parser)
filename = sys.argv[1]
lp_parser.parse_file(f"{filename}")

solver = SimplexSolver(pivot_rule="Bland")

print(solver.solve(lp_parser))