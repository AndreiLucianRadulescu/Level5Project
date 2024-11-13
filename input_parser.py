from fractions import Fraction

# Class that defines a parser for .lp files, i.e. files that contain optimization programs.
class LPParser:
    def __init__(self):
        self.num_variables = 0
        self.num_constraints = 0
        self.variables = set()
        self.constraints = {}
        self.obj_function = {}
        
    def parse_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Remove empty lines
        non_empty_lines = [line.strip() for line in lines if (line != '' and line != '\n' and (not line.startswith('\\')))]
        
        line_idx = 0
        while non_empty_lines[line_idx] != 'End':
            line = non_empty_lines[line_idx]

            if line == "Maximize":
                # Assume only one objective function, could extend later.
                # Also, remove whitespace in the next line.
                self.parse_obj_function(non_empty_lines[line_idx + 1].replace(' ', ''), filename)
                line_idx += 2
            
            elif line == "Subject To":
                line_idx = self.parse_constraints(non_empty_lines, line_idx + 1, filename)
        
            # Now we have all constraints, and the objective function.
            # However, need to update number of variables now, as maybe the objective function or constraints
            # don't contain all variables

    def parse_obj_function(self, string_to_parse, filename):
        parts = string_to_parse.split(":")

        if len(parts) < 2:
            raise Exception(f"Invalid objective function in {filename}.")

        # Assume everything is +, will do more later.
        terms = self.preprocess_terms(parts[1])
        terms = [t for t in terms.split('+') if t != '']
        for term in terms:
            coefficient, variable = self.split_coefficient_and_variable(term)

            if coefficient == variable == None:
                raise Exception(f"Invalid term in the objective function in {filename}.")
            
            if variable not in self.variables:
                self.num_variables += 1
                self.variables.add(variable)
            self.obj_function[variable] = coefficient

    def split_coefficient_and_variable(self, expr):
        idx = 0

        try:
            coefficient = ''
            while idx < len(expr) and ('0' <= (expr[idx]) <= '9' or expr[idx] in ['-', '.', '/']):
                coefficient += expr[idx]
                idx += 1

            if idx == 0:
                coefficient = Fraction(1)

            elif idx == 1 and expr[0] == '-':
                coefficient = Fraction(-1)

            else:
                coefficient = Fraction(coefficient)

            return coefficient, expr[idx:]
        except:
            return None, None
        
    def preprocess_terms(self, terms_str):
        terms_str = terms_str.replace('-', '+-')
        return terms_str
    
    def parse_constraints(self, lines, starting_idx, filename):
        # Iterate until the "End". To be changed when I add bounds.
        for line_idx in range(starting_idx, len(lines) - 1):
            line = lines[line_idx].replace(' ', '')
            parts = line.split(':')
            self.constraints[parts[0]] = {}

            terms, bound = parts[1].split('<=')
            self.constraints[parts[0]]['rhs'] = Fraction(bound)
            terms = self.preprocess_terms(terms)
            terms = [t for t in terms.split('+') if t != '']

            for term in terms:
                coefficient, variable = self.split_coefficient_and_variable(term)
                if coefficient == variable == None:
                    raise Exception(f"Invalid term in constraint {parts[0]} in {filename}.")
                
                if variable not in self.variables:
                    self.num_variables += 1
                    self.variables.add(variable)
                self.constraints[parts[0]][variable] = coefficient
            
            self.num_constraints += 1
        
        return len(lines) - 1

    def stringify_equation(self, equation_dict):
        result = []
        for variable, coefficient in equation_dict.items():
            if variable == 'rhs':
                continue
            result.append(str(coefficient) + variable)

        return "+".join(result)

    def __str__(self):
        if not self.num_variables:
            return 'Number of variables is 0. Make sure to use the parse_file on a valid .lp linear program.'
        
        else:
            result = ""
            result += '=====================\n'
            result += f"Variables: \n{sorted(list(self.variables))}\n"
            result += '=====================\n'
            result += f"Constraints:\n"
            for constraint in self.constraints:
                result += self.stringify_equation(self.constraints[constraint])
                result += ' <= ' + self.constraints[constraint]['rhs'] + '\n'
            result += '=====================\n'
            result += 'Objective Function:\n'
            result += self.stringify_equation(self.obj_function) + '\n'

            return result
