from input_parser import LPParser
import numpy as np
from fractions import Fraction
import math

class SimplexSolver:
    def __init__(self, pivot_rule: str):
        self.pivot_rule = pivot_rule

    def get_tableau_from_lp(self, lp_parser: LPParser):
        self.num_constraints = len(lp_parser.constraints)
        self.num_variables = len(lp_parser.variables)

        # We need num_constraints + 1 rows because we have one more row for the objective function
        # We need num_variables + len(num_constraints) + 1 because for each constraint, we would have a slack variable, 
        # as all constraints are of type <= for now, and also one more column for the rhs of the constraints
        tableau = np.full((self.num_constraints + 1, self.num_variables + self.num_constraints + 1), Fraction(0), dtype=object)
        list_of_variables = sorted(list(lp_parser.variables))

        i = 0
        for constraint_name, var_dict in lp_parser.constraints.items():
            for variable, coefficient in var_dict.items():
                if variable in lp_parser.variables:
                    j = list_of_variables.index(variable)

                    tableau[i, j] = coefficient
            
            tableau[i, -1] = lp_parser.constraints[constraint_name]['rhs']
            tableau[i, i + self.num_variables] = Fraction(1)
            i += 1

        for variable, coefficient in lp_parser.obj_function.items():
            if variable in lp_parser.variables:
                j = list_of_variables.index(variable)

                tableau[-1, j] = -coefficient

        # Add a slack variable for each constraint.
        self.list_of_variables = list_of_variables + [f's{i+1}' for i in range(self.num_constraints)]
        return tableau 

    def solve(self, lp_parser: LPParser):
        tableau = self.get_tableau_from_lp(lp_parser)
        current_basis = self.list_of_variables[self.num_variables:]
        visited_states = set()
        visited_states.add(tuple(current_basis))
        
        while True:
            # if tuple(current_basis) in visited_states:
            #     print('Cycle detected. Exiting.')
            #     return
            # else:
            #     visited_states.add(tuple(current_basis))

            pivot_column = self.find_entering_variable(tableau)

            if pivot_column == -1:
                break

            # Calculate the ratios for the pivot operation
            denominator = tableau[:-1, pivot_column]

            ratios = []
            # Use for loop, as np.where does not really work on Fractions.
            for i in range(len(denominator)):
                if denominator[i] != 0:
                    ratios.append(tableau[i, -1] / denominator[i])
                else:
                    ratios.append(Fraction(-1))

            ratios = np.array(ratios)
            # Only consider positive ratios
            positive_ratios = ratios[ratios > 0]
            
            if positive_ratios.size == 0:
                # If no positive ratio, we have to make a degenerate move.

                if ratios[ratios == 0].size == 0:
                    return {"status": "Unbounded", "value": math.inf}
                
                # If we have at least a ratio of 0, make any degenerate move
                # (the first one in this case).
                leaving_variable_index = np.where(ratios == 0)[0][0]

            else:
                # If we have a positive ratio, can make an improving move.

                # Get the index of leaving variable
                leaving_variable_index = np.argmin(positive_ratios)
                leaving_variable_index = np.where(ratios == positive_ratios[leaving_variable_index])[0][0]

            self.perform_pivot_operation(tableau, pivot_column, leaving_variable_index)
        
        return {"status": "Optimal", "value": float(tableau[-1, -1])}
   
    def perform_pivot_operation(self, tableau, pivot_column: int, leaving_variable_index: int):
        # Set the pivot row to have 1 in the pivot column.
        tableau[leaving_variable_index, :] *= (1 / tableau[leaving_variable_index, pivot_column])

        for i in range(tableau.shape[0]):
            if i == leaving_variable_index:
                continue

            if tableau[i, pivot_column] == 0:
                continue

            tableau[i, :] -= tableau[leaving_variable_index, :] * tableau[i, pivot_column]


    def find_entering_variable(self, tableau):
        # Find the index of the smallest negative coefficient.
        if self.pivot_rule == "Dantzig":
            pivot_column = np.argmin(tableau[-1, :])
        
        # Find the index of the first negative coefficient.
        elif self.pivot_rule == "Bland":
            pivot_column = np.argmax(tableau[-1, :] < 0)
        
        if tableau[-1, pivot_column] >= 0:
            # Signifies end of computations.
            return -1

        return pivot_column
    