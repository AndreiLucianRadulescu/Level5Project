import random
import numpy as np

class DenseLPGenerator:
    def __init__(self, precision=2):
        self.precision = precision
    
    def generate_constraint(self, num_variables, scale_factor=5):
        """Generate a constraint that's guaranteed to be satisfied by the origin."""
        coefficients = np.array([random.uniform(-1, 1) for _ in range(num_variables)])
        coefficients = coefficients / np.linalg.norm(coefficients)
        
        # Scale coefficients to make them more meaningful
        coefficients *= scale_factor
        
        rhs = random.uniform(0, 10)  # Only positive RHS values
        
        return coefficients, rhs
    
    def generate_dense_lp(self, filepath, num_variables, num_constraints, maximize=True):
        """
        Generate a dense linear program with origin as a feasible point.
        
        Args:
            filepath: Path to save the LP file
            num_variables: Number of decision variables
            num_constraints: Number of constraints
            maximize: True for maximization, False for minimization
        """
        with open(filepath, 'w') as f:
            f.write('Maximize\n' if maximize else 'Minimize\n')
            
            # Generate and write objective function
            f.write(' obj: ')
            obj_coefficients = np.array([random.uniform(-1, 1) for _ in range(num_variables)])
            obj_coefficients = obj_coefficients / np.linalg.norm(obj_coefficients) * 10  # Scale for better numerics
            
            for i, coef in enumerate(obj_coefficients):
                coef = round(coef, self.precision)
                if i == 0:
                    f.write(f'{coef}x{i+1} ')
                else:
                    f.write(f'{" + " if coef >= 0 else " "}{coef}x{i+1} ')
            
            # Write constraints
            f.write('\nSubject To\n')
            for i in range(num_constraints):
                coefficients, rhs = self.generate_constraint(num_variables)
                f.write(f' c{i+1}: ')
                
                for j, coef in enumerate(coefficients):
                    coef = round(coef, self.precision)
                    if j == 0:
                        f.write(f'{coef}x{j+1} ')
                    else:
                        f.write(f'{" + " if coef >= 0 else " "}{coef}x{j+1} ')
                
                f.write(f'<= {round(rhs, self.precision)}\n')
            
            f.write('End')
    
    
           
