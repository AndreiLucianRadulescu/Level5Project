from input_parser import LPParser
import numpy as np
from fractions import Fraction
import math
import re

class SimplexSolver:
    def __init__(self, pivot_rule: str):
        self.pivot_rule = pivot_rule
        self.solution = None

    def solve(self, lp_parser: LPParser):
        self.num_constraints = len(lp_parser.constraints)
        self.num_variables = len(lp_parser.variables)

        self.negative_rhs_idxs = {i: 0 for i in range(len(lp_parser.constraints)) if lp_parser.constraints[i]['rhs'] < 0}
        
        tableau = np.full((self.num_constraints + 1, self.num_variables + self.num_constraints + 1 + len(self.negative_rhs_idxs)), Fraction(0), dtype=object)
        self.original_variables = sorted(list(lp_parser.variables), key=lambda x: self.sort_variables_key_function(x))

        i = 0
        for constraint_idx, var_dict in enumerate(lp_parser.constraints):
            if constraint_idx in self.negative_rhs_idxs:
                sign = -1
            else:
                sign = 1    

            for variable, coefficient in var_dict.items():
                if variable in lp_parser.variables:
                    j = self.original_variables.index(variable)

                    tableau[i, j] = coefficient * sign
            
            tableau[i, -1] = lp_parser.constraints[constraint_idx]['rhs'] * sign

            # Here we add slack variables (or surplus variable, denoted by a -1 coefficient.)
            tableau[i, i + self.num_variables] = Fraction(1) * sign
            i += 1
        
        # Here we set the coefficients of the artificial variables (if there are any)
        art_var_added = 0

        for i, neg_idx in enumerate(self.negative_rhs_idxs):
            tableau[neg_idx, len(self.original_variables) + self.num_constraints + art_var_added] = 1
            art_var_added += 1

        # Now we set all variables as such:
        #   - original variables,
        #   - slack variables, denoted by _sNumber,
        #   - artificial variables (if we need two phase simplex), denoted by _zzzNumber.
        self.all_variables = self.original_variables + [f'_s{i+1}' for i in range(self.num_constraints)] + [f'_zzz{i+1}' for i in range(len(self.negative_rhs_idxs))]

        # Now we need to set the objective function (last row in tableau)
        # If we have artificial variables, we need to set the objective function
        # as the preliminary one, asking to maximize -1 * the sum of all artificial variables.
        art_var_added = 0
        if len(self.negative_rhs_idxs) > 0:
            for neg_idx, i in self.negative_rhs_idxs.items():
                print(neg_idx)
                tableau[-1, self.num_variables + self.num_constraints + art_var_added] = 1
                art_var_added += 1
                tableau[-1] -= tableau[neg_idx]

            current_basis = ['0' for i in range(self.num_constraints)]

            num_a_var_alrdy_in_basis = 0
            for i in range(self.num_constraints):
                if i in self.negative_rhs_idxs:
                    current_basis[i] = self.all_variables[self.num_constraints + self.num_variables + num_a_var_alrdy_in_basis]
                    num_a_var_alrdy_in_basis += 1
                else:
                    current_basis[i] = self.all_variables[self.num_variables + i]

            temp_solution = self.solve_tableau(tableau, current_basis)
            
            # We are now done with Phase 1.
            if temp_solution["status"] != "Optimal" or temp_solution["value"] != 0:
                self.solution = "Infeasible"
                return {"status": "Infeasible", "value": - np.inf, "num_pivot_steps": num_pivot_steps}
            print('FINISHED PHASE 1 \n\n\n\n')
            for row in tableau[-1:,]:
                print('obj row')
                print(row, end = ' ')
                print()
                print(self.all_variables)
                print()
            print('\n\n\n')
            # If we get here, then need to proceed to Phase 2.
            #tableau = np.delete(tableau, np.array([i for i in range(self.num_variables + self.num_constraints, len(self.all_variables))]), axis = 1)
            current_basis = temp_solution["current_basis"]
            # tableau = np.delete(tableau, [3], axis=1)
            # current_basis.remove('_s3')
            print('HERE' + str(current_basis))

            tableau[-1] = Fraction(0)

            for variable, coefficient in lp_parser.obj_function.items():
                tableau[-1, self.all_variables.index(variable)] = - coefficient
            tableau = np.delete(tableau, [3, 4], axis=1)
            self.all_variables.remove('_s1')
            self.all_variables.remove('_s2')
            print(self.all_variables)
            # # We have initialised the new objective function.
            # # Now we need to make basis variables have only one value of 1 on column.
            # for idx, basic_variable in enumerate(current_basis):
            #     basic_variable_idx = self.all_variables.index(basic_variable)

            #     tableau[-1] -= tableau[idx] * tableau[-1, basic_variable_idx]
            #print(self.ensure_basis(tableau, current_basis))
            tableau[-1] += 5 * tableau[3]
            tableau[-1] -= 4 * tableau[0]
            tableau
            for row in tableau:
                for col in row:
                    print(col, end = ' ')
                print()
            print()
            print(current_basis)
            print('\n\n\n')
            return self.solve_tableau(tableau, current_basis)
        else:
            for variable, coefficient in lp_parser.obj_function.items():
                tableau[-1, self.all_variables.index(variable)] = - coefficient
            current_basis = self.all_variables[self.num_variables:]

            return self.solve_tableau(tableau, current_basis) 
   
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
        negative_indices = np.where(tableau[-1, :-1] < 0)[0]
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
    
    def solve_tableau(self, tableau, current_basis):
        visited_states = set()

        num_pivot_steps = 0
        while True:
            for row in tableau:
                for col in row:
                    print(col, end = ' ')
                print()
            # print(current_basis)
            # if not self.ensure_basis(tableau, current_basis):
            #     return 'WRONG'
            print('\n\n\n\n')
            if tuple(current_basis) in visited_states:
                print('Cycle detected. Exiting.')
                return {"status": "Unsolvable (cycles)", "value": - math.inf, "num_pivot_steps": num_pivot_steps, "current_basis": current_basis}
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
                    return {"status": "Unbounded", "value": math.inf, "num_pivot_steps": num_pivot_steps, "current_basis": current_basis}
                
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
    
        return {"status": "Optimal", "value": float(tableau[-1, -1]), "num_pivot_steps": num_pivot_steps, "current_basis": current_basis}

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
    
    def ensure_basis(self, tableau, current_basis):
        for variable in current_basis:
            if np.sum(tableau[:, self.all_variables.index(variable)]) != 1:
                return False

        return True