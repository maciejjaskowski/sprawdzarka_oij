# Sprawdzarka - Python Script Tester

This is a tool that checks the correctness of a Python script by running it against a series of input/output test cases.

## Usage

```bash
python sprawdz.py <python_script> <test_directory>
```

Where:
- `<python_script>` is the path to the Python script you want to test
- `<test_directory>` is a directory containing test cases

## Test Directory Format

The test directory should contain pairs of files:
- `*.in` files: Input data that will be fed to the script
- `*.out` files: Expected output that should match the script's output

For each input file `test_name.in`, there should be a corresponding output file `test_name.out`.

## Output Format

The program outputs:
- A sequence of `.` (for passed tests) and `X` (for failed tests)
- Execution time for each test
- A summary of how many tests passed

## Example

```bash
python sprawdz.py sample_script.py test_cases
```

## Sample Script

A sample script `sample_script.py` and test cases are included to demonstrate the functionality. 