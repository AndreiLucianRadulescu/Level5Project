import random

class DenseLPGenerator():
    def __init__(self, precision):
        self.precision = precision
    
    def generate_dense_lp(self, filepath, num_variables, num_constraints, maximize = True):
        with open(filepath, 'w') as f:
            if maximize:
                f.write('Maximize')
            else:
                f.write('Minimize')
            
            f.write('\n')

            # Now write the objective function:
            f.write(' obj: ')
            for i in range(num_variables):
                random_coefficient = round(random.uniform(-1, 1), self.precision)
                if random_coefficient < 0:
                    temp = ''
                else:
                    temp = '+'

                f.write(f'{temp}{random_coefficient}x{i+1} ')
            f.write('\nSubject To\n')
            for i in range(num_constraints):
                f.write(f' c{i+1}: ')

                for i in range(num_variables):
                    random_coefficient = round(random.uniform(-1, 1), self.precision)
                    if random_coefficient < 0:
                        temp = ''
                    else:
                        temp = '+'
                    
                    f.write(f'{temp}{random_coefficient}x{i+1} ')
            
                f.write(f'<= {round(random.uniform(-1, 1), self.precision)}\n')

            f.write('End')
