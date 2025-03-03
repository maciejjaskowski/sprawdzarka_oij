#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import argparse

def normalize_output(text):
    """
    Normalize output text by:
    1. Converting all line endings to \n
    2. Stripping trailing whitespace from each line
    3. Stripping leading/trailing empty lines
    """
    # Normalize line endings
    text = text.replace('\r\n', '\n')
    
    # Split into lines, strip each line, and join back
    lines = [line.rstrip() for line in text.split('\n')]
    
    # Remove any leading/trailing empty lines
    while lines and lines[0] == '':
        lines.pop(0)
    while lines and lines[-1] == '':
        lines.pop()
        
    # Join back with newlines
    return '\n'.join(lines)

def run_tests(python_script, test_dir, timeout=10):
    """
    Run tests for a Python script against input/output pairs in a directory.
    
    Args:
        python_script: Path to Python script to test
        test_dir: Directory containing .in and .out test files
        timeout: Timeout in seconds for each test (default: 10)
    """
    # Check if script exists
    if not os.path.isfile(python_script):
        print(f"Error: Python script '{python_script}' not found.")
        sys.exit(1)
    
    # Check if directory exists
    if not os.path.isdir(test_dir):
        print(f"Error: Test directory '{test_dir}' not found.")
        sys.exit(1)
        
    # Get all .in files
    in_files = [f for f in os.listdir(test_dir) if f.endswith('.in')]
    in_files.sort()  # Sort files for predictable order
    
    results = []
    times = []
    
    # Print initial message
    print(f"Running tests from {test_dir} with timeout {timeout}s:")
    
    # Process each test case
    for in_file in in_files:
        base_name = in_file[:-3]  # Remove .in extension
        out_file = base_name + '.out'
        
        # Skip if no corresponding .out file
        if out_file not in os.listdir(test_dir):
            print(f"Warning: No output file found for {in_file}, skipping.")
            continue
        
        # Full paths
        in_path = os.path.join(test_dir, in_file)
        out_path = os.path.join(test_dir, out_file)
        
        # Run the test
        with open(in_path, 'r') as input_file:
            # Measure execution time
            start_time = time.time()
            try:
                # Run the script with input from .in file
                completed_process = subprocess.run(
                    ['python3', python_script], 
                    stdin=input_file,
                    capture_output=True,
                    text=True,
                    timeout=timeout  # Use the provided timeout value
                )
                execution_time = time.time() - start_time
                
                # Get expected output
                with open(out_path, 'r') as output_file:
                    expected_output = output_file.read()
                
                # Normalize both outputs before comparison
                actual_output = normalize_output(completed_process.stdout)
                expected_output = normalize_output(expected_output)
                
                if actual_output == expected_output:
                    result = '.'
                else:
                    result = 'X'
                
                # Print result immediately
                print(result, end='', flush=True)
                
                results.append(result)
                times.append(execution_time)
                
            except subprocess.TimeoutExpired:
                print('T', end='', flush=True)  # T for timeout, print immediately
                results.append('T')
                times.append(timeout)
            except Exception as e:
                print('E', end='', flush=True)  # E for error, print immediately
                results.append('E')
                times.append(0.0)
    
    # Print a newline after all test results
    print()
    
    # Print execution times
    print("\nExecution times:")
    for i, (in_file, t) in enumerate(zip(in_files, times)):
        print(f"{in_file}: {t:.3f}s - {'PASS' if results[i] == '.' else 'FAIL'}")
    
    # Print summary
    successful = results.count('.')
    total = len(results)
    print(f"\nSummary: {successful}/{total} tests passed")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Test a Python script against input/output test cases')
    parser.add_argument('script', help='Path to the Python script to test')
    parser.add_argument('testdir', help='Directory containing test cases (.in and .out files)')
    parser.add_argument('-t', '--timeout', type=float, default=10, 
                        help='Timeout in seconds for each test (default: 10)')
    
    args = parser.parse_args()
    
    run_tests(args.script, args.testdir, args.timeout)

if __name__ == "__main__":
    main()
