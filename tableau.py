# Class that defines a tableau for Simplex. Implementation using basic lists rather than numpy arrays.
from input_parser import LPParser
import numpy as np

class Tableau:
    def __init__(self, lp_parser: LPParser):
        num_constraints = len(lp_parser.constraints)
        num_variables = len(lp_parser.variables)

        # We need num_constraints + 1 rows because we have one more row for the objective function
        # We need num_variables + len(num_constraints) + 1 because for each constraint, we would have a slack variable, 
        # as all constraints are of type <= for now, and also one more column for the rhs of the constraints
        self.tableau = np.zeros((num_constraints+1, num_variables+num_constraints+1))
        list_of_variables = sorted(list(lp_parser.variables))

        i = 0
        for constraint_name, var_dict in lp_parser.constraints.items():
            print(var_dict)
            for variable, coefficient in var_dict.items():
                if variable in lp_parser.variables:
                    j = list_of_variables.index(variable)

                    self.tableau[i, j] = coefficient
            
            self.tableau[i, -1] = lp_parser.constraints[constraint_name]['rhs']
            self.tableau[i, i + num_constraints] = 1
            i += 1

        for variable, coefficient in lp_parser.obj_function.items():
            if variable in lp_parser.variables:
                j = list_of_variables.index(variable)

                self.tableau[-1, j] = -coefficient

    def __str__(self):
        return str(self.tableau)
    
    def multiply_row(self, row_idx, value):
        self.tableau[row_idx] *= value

    def multiply_column(self, col_idx, value):
        self.tableau[:, col_idx] *= value