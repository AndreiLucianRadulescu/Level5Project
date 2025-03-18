import sys
from input_parser import LPParser
from simplex_solver import SimplexSolver
import time

lp_parser = LPParser()
# print(lp_parser)
filename = sys.argv[1]
lp_parser.parse_file(f"{filename}")
solver = SimplexSolver(pivot_rule="SteepestEdge")

start_time = time.time()
print(solver.solve(lp_parser))
end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)
print(f"Elapsed time: {elapsed_time:.6f} seconds")