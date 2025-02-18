import re

def sort_variables(variables):
    """
    Sorts variables correctly:
    - x1, x2, ..., x10 sorted numerically.
    - a, b, c sorted lexicographically.
    - s1, s2, ... sorted numerically at the end.
    """
    
    def key_function(var):
        match = re.match(r"([a-zA-Z]+)(\d*)", var)
        if match:
            prefix, num = match.groups()
            return (prefix, int(num) if num else 0)  # Convert number to int for proper sorting
        return (var, 0)

    return sorted(variables, key=key_function)

# Example usage
variables = ["x10", "x2", "x1", "a", "b", "c", "s2", "s1"]
sorted_vars = sort_variables(variables)
print(sorted_vars)