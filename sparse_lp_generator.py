import random
import numpy as np

class SparseLPGenerator:
    def __init__(self, precision=2, allow_negative_rhs=False, density=0.5):
        """
        Initialize the SparseLPGenerator.
        
        Args:
            precision: Number of decimal places in coefficients and RHS
            allow_negative_rhs: Whether to allow negative RHS values
            density: Value between 0 and 1, representing the fraction of non-zero coefficients
        """
        self.precision = precision
        self.allow_negative_rhs = allow_negative_rhs
        self.density = density
   
    def generate_sparse_coefficients(self, num_variables, scale_factor=5):
        """
        Generate sparse coefficients with the initialized density level.
        
        Args:
            num_variables: Number of variables
            scale_factor: Factor to scale coefficients by
            
        Returns:
            Sparse coefficient array
        """
        # Determine how many coefficients should be non-zero
        num_nonzero = max(1, int(num_variables * self.density))
        
        # Create sparse array with zeros
        coefficients = np.zeros(num_variables)
        
        # Randomly select indices for non-zero coefficients
        nonzero_indices = random.sample(range(num_variables), num_nonzero)
        
        # Set non-zero values
        for idx in nonzero_indices:
            coefficients[idx] = random.uniform(-1, 1)
        
        # Normalize if not all zeros (avoid division by zero)
        if np.linalg.norm(coefficients) > 0:
            coefficients = coefficients / np.linalg.norm(coefficients)
            
        # Scale coefficients with randomized scale factor for variety
        coefficients *= random.uniform(1, scale_factor)
        
        return coefficients
        
    def generate_constraint(self, num_variables, scale_factor=5):
        """Generate a sparse constraint that's guaranteed to be satisfied by the origin."""
        coefficients = self.generate_sparse_coefficients(num_variables, scale_factor)
       
        if self.allow_negative_rhs:
            rhs = random.uniform(-10, 10)
        else:
            rhs = random.uniform(0, 10)  # Only positive RHS values
       
        return coefficients, rhs
   
    def generate_sparse_lp(self, filepath, num_variables, num_constraints, maximize=True):
        """
        Generate a sparse linear program with origin as a feasible point.
       
        Args:
            filepath: Path to save the LP file
            num_variables: Number of decision variables
            num_constraints: Number of constraints
            maximize: True for maximization, False for minimization
        """
        with open(filepath, 'w') as f:
            f.write('Maximize\n' if maximize else 'Minimize\n')
           
            # Generate and write sparse objective function
            f.write(' obj: ')
            obj_coefficients = self.generate_sparse_coefficients(num_variables, scale_factor=10)
           
            first_term = True
            for i, coef in enumerate(obj_coefficients):
                coef = round(coef, self.precision)
                if coef == 0:
                    continue
                    
                if first_term:
                    f.write(f'{coef}x{i+1} ')
                    first_term = False
                else:
                    f.write(f'{" + " if coef >= 0 else " "}{coef}x{i+1} ')
           
            # If objective is empty, add a dummy term
            if first_term:
                f.write(f'0x1 ')
           
            # Write constraints
            f.write('\nSubject To\n')
            for i in range(num_constraints):
                coefficients, rhs = self.generate_constraint(num_variables)
                f.write(f' c{i+1}: ')
               
                first_term = True
                for j, coef in enumerate(coefficients):
                    coef = round(coef, self.precision)
                    if coef == 0:
                        continue
                        
                    if first_term:
                        f.write(f'{coef}x{j+1} ')
                        first_term = False
                    else:
                        f.write(f'{" + " if coef >= 0 else " "}{coef}x{j+1} ')
               
                # If all coefficients are zero, add a dummy constraint to avoid syntax errors
                if first_term:
                    f.write(f'0x1 ')
                    
                f.write(f'<= {round(rhs, self.precision)}\n')
           
            # Add variable bounds
            f.write('Bounds\n')
            for i in range(num_variables):
                f.write(f' 0 <= x{i+1}\n')
                
            f.write('End')

# Example usage:
generator = SparseLPGenerator(precision=4, density=0.5)  # 30% density
generator.generate_sparse_lp("sparse_problem.lp", num_variables=100, num_constraints=100)