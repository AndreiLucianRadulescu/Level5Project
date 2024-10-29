from tableau import Tableau
from input_parser import LPParser
import numpy as np

class SimplexSolver:
    def __init__(self, pivot_rule: str):
        self.pivot_rule = pivot_rule

    def solve(self, lp_parser: LPParser):
        tableau = Tableau(lp_parser)
        
        while True:
            pivot_column = self.find_entering_variable(tableau)

            if pivot_column == -1:
                print('Optimal solution has been found.')
                break
            
            denominator = tableau[:-1, pivot_column]
            ratios = np.where(denominator > 0, tableau[:-1, -1] / denominator, np.inf)

            leaving_variable_index = -1
            leaving_variable_index = np.argmin(ratios[ratios > 0])

            # If all ratios are infinity, it means that the problem is unbounded
            if leaving_variable_index == -1 or ratios[leaving_variable_index] == np.inf:
                print('The solution is unbounded.')
                return

            # Now we found leaving variable (denoted by leaving_variable_index). Now we just have to adjust the tableau.
            self.adjust_tableau(pivot_column, leaving_variable_index)

        print(f'The maximum value of the objective function is {tableau[-1, -1]}')

    def adjust_tableau(self, pivot_column, leaving_variable_index):


    def find_entering_variable(self, tableau):
        if self.pivot_rule == "Dantzig":
            pivot_column = np.argmin(tableau[-1, :])

            if tableau[-1, pivot_column] >= 0:
                # Signifies end of computations.
                return -1
            
            return pivot_column
    