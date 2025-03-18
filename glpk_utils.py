import subprocess
import time
import os
import json
from tqdm import tqdm

def solve_problem_with_glpsol(file_path):
    """
    Solve a given LP problem using both GLPK simplex and interior point methods via glpsol.
    
    Args:
        file_path: Path to the LP problem file (.mps or other supported format)
        
    Returns:
        dict: A dictionary containing status, simplex_time, and interior_point_time
    """
    results = {}
    
    # SIMPLEX
    start_time = time.time()
    simplex_process = subprocess.run(
        ["glpsol", "--lp", file_path, "--simplex"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    simplex_time = time.time() - start_time
    
    simplex_output = simplex_process.stdout + simplex_process.stderr
    status = "undefined"

    if "OPTIMAL LP SOLUTION FOUND" in simplex_output:
        status = "optimal"
    elif "LP HAS UNBOUNDED PRIMAL SOLUTION" in simplex_output:
        status = "unbounded"
    elif "LP HAS NO FEASIBLE SOLUTION" in simplex_output:
        status = "infeasible"
    elif "LP HAS NO PRIMAL FEASIBLE SOLUTION" in simplex_output:
        status = "infeasible"
    
    results['status'] = status
    results['simplex_time'] = simplex_time
    results['simplex_return_code'] = simplex_process.returncode

    # IPM
    start_time = time.time()
    interior_process = subprocess.run(
        ["glpsol", "--lp", file_path, "--interior"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    interior_time = time.time() - start_time
    
    results['interior_point_time'] = interior_time
    results['interior_return_code'] = interior_process.returncode
    
    return results

def process_problem_set(problem_dir, output_json_path):
    """
    Process all problems in a directory and save results to a JSON file.
    
    Args:
        problem_dir: Directory containing problem files
        output_json_path: Path to save the JSON results
    """
    results = {}
    problem_files = [f for f in os.listdir(problem_dir) if os.path.isfile(os.path.join(problem_dir, f))]
    
    for i in tqdm(range(len(problem_files))):
        problem_file = problem_files[i]
        file_path = os.path.join(problem_dir, problem_file)
        
        try:
            problem_results = solve_problem_with_glpsol(file_path)
            results[problem_file] = problem_results
        except Exception as e:
            print(f"Error solving {problem_file}: {str(e)}")
            results[problem_file] = {
                "status": "error",
                "error_message": str(e),
                "simplex_time": None,
                "interior_point_time": None
            }
    
    with open(output_json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results