"""Add two numbers given on the command line."""
import sys

a, b = float(sys.argv[1]), float(sys.argv[2])
print(f"{a} + {b} = {a + b}")
