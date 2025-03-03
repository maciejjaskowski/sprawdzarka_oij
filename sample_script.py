#!/usr/bin/env python3
"""
A simple script that reads two numbers from stdin and prints their sum.
This will be used to test our checking program.
"""

def main():
    try:
        # Read two numbers from stdin
        a = int(input().strip())
        b = int(input().strip())
        
        # Calculate and print the sum
        # Note: This has a deliberate bug for test demonstration
        # It adds 1 to the sum, so some tests will fail
        result = a + b + 1  # The correct version would be: result = a + b
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 