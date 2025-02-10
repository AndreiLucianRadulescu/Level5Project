from input_parser import LPParser
import numpy as np
from fractions import Fraction
import math
import re

class SimplexSolver:
    def __init__(self, pivot_rule: str):
        self.pivot_rule = pivot_rule
        self.solution = None

    def get_tableau_from_lp(self, lp_parser: LPParser):
        self.num_constraints = len(lp_parser.constraints)
        self.num_variables = len(lp_parser.variables)

        # We need num_constraints + 1 rows because we have one more row for the objective function
        # We need num_variables + len(num_constraints) + 1 because for each constraint, we would have a slack variable, 
        # as all constraints are of type <= for now, and also one more column for the rhs of the constraints
        tableau = np.full((self.num_constraints + 1, self.num_variables + self.num_constraints + 1), Fraction(0), dtype=object)
        self.original_variables = sorted(list(lp_parser.variables), key=lambda x: self.sort_variables_key_function(x))

        i = 0
        for constraint_name, var_dict in lp_parser.constraints.items():
            for variable, coefficient in var_dict.items():
                if variable in lp_parser.variables:
                    j = self.original_variables.index(variable)

                    tableau[i, j] = coefficient
            
            tableau[i, -1] = lp_parser.constraints[constraint_name]['rhs']
            tableau[i, i + self.num_variables] = Fraction(1)
            i += 1

        for variable, coefficient in lp_parser.obj_function.items():
            if variable in lp_parser.variables:
                j = self.original_variables.index(variable)

                tableau[-1, j] = -coefficient

        # Add a slack variable for each constraint.
        self.all_variables = self.original_variables + [f'_s{i+1}' for i in range(self.num_constraints)]
        return tableau 

    def solve(self, lp_parser: LPParser):
        tableau = self.get_tableau_from_lp(lp_parser)
        current_basis = self.all_variables[self.num_variables:]
        visited_states = set()

        num_pivot_steps = 0
        while True:
            if tuple(current_basis) in visited_states:
                print('Cycle detected. Exiting.')
                return
            else:
                visited_states.add(tuple(current_basis))

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
                    self.solution = "Unbounded"
                    return {"status": "Unbounded", "value": math.inf, "num_pivot_steps": num_pivot_steps}
                
                # If we have at least a ratio of 0, make any degenerate move
                # (the first one in this case).
                leaving_variable_index = np.where(ratios == 0)[0][0]

            else:
                # If we have a positive ratio, can make an improving move.

                # Get the index of leaving variable
                leaving_variable_index = np.argmin(positive_ratios)
                leaving_variable_index = np.where(ratios == positive_ratios[leaving_variable_index])[0][0]

            self.perform_pivot_operation(tableau, pivot_column, leaving_variable_index)

            # Update state
            num_pivot_steps += 1
            entering_variable = self.all_variables[pivot_column]
            current_basis[leaving_variable_index] = entering_variable

        self.solution = {current_basis[i]: float(tableau[i, -1]) for i in range(len(current_basis)) if current_basis[i] in self.original_variables}
        return {"status": "Optimal", "value": float(tableau[-1, -1]), "num_pivot_steps": num_pivot_steps}
   
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
        negative_indices = np.where(tableau[-1, :] < 0)[0]
        
        if len(negative_indices) == 0:
            return -1  # No negative coefficients, end of computations.
        
        # Smallest negative coefficient
        if self.pivot_rule == "Dantzig":
            pivot_column = negative_indices[np.argmin(tableau[-1, negative_indices])]
        
        # First negative coefficient (smallest index)
        elif self.pivot_rule == "Bland":
            pivot_column = negative_indices[0]
        
        # Random negative coefficient
        elif self.pivot_rule == "Random":
            pivot_column = np.random.choice(negative_indices)

        return pivot_column
    
    def get_solution(self):
        if self.solution is None:
            print('No LP has been solved yet, thus returning -1.')
            return -1
        
        return self.solution
    
    def sort_variables_key_function(self, var):
        """
        This function sorts the variables as such:
            - x1, x2, ..., x10 -> x1, x2, ..., x10
            - a, c, b, d -> a, b, c, d
        Need this function to handle both variables without digits in their name, but also those with digits.
        """
        match = re.match(r"([a-zA-Z]+)(\d*)", var)
        if match:
            prefix, num = match.groups()
            return (prefix, int(num) if num else 0)  # Convert number to int for proper sorting
        return (var, 0)