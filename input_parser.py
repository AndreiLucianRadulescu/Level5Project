# Class that defines a parser for .lp files, i.e. files that contain optimization programs.

class LPParser:
    headings = set(["Maximize", "Subject To", "Bounds", "Generals", "End"])

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
        non_empty_lines = [line.strip() for line in lines if (line != '' and line != '\n')]
        print(non_empty_lines)
        line_idx = 0
        line = non_empty_lines[line_idx]
        while line != 'End':
            if line.startswith('\\') or line == '\n' or line == "":
                continue

            elif line == "Maximize":
                self.parse_obj_function(lines[line_idx + 1].replace(' ', ''), filename)
            


    def parse_obj_function(self, string_to_parse, filename):
        parts = string_to_parse.split(":")

        if len(parts) < 1:
            raise Exception(f"Invalid objective function in {filename}.")

        print(parts[1])
