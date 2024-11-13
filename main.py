import sys
from input_parser import LPParser
from simplex_solver import SimplexSolver

lp_parser = LPParser()
# print(lp_parser)
filename = sys.argv[1]
lp_parser.parse_file(f"./problems/{filename}")

solver = SimplexSolver(pivot_rule="Dantzig")

solver.solve(lp_parser)