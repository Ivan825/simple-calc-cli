# app.py
import sys

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def parse_and_run(argv):
    """
    Usage: python app.py <op> <num1> <num2>
    op: add | sub | mul | div
    Returns numeric result (float for division/add)
    """
    if len(argv) != 4:
        raise ValueError("Usage: app.py <op> <num1> <num2>")
    op = argv[1].lower()
    try:
        a = float(argv[2])
        b = float(argv[3])
    except ValueError:
        raise ValueError("num1 and num2 must be numbers")

    ops = {
        "add": add,
        "sub": sub,
        "mul": mul,
        "div": div
    }
    if op not in ops:
        raise ValueError(f"Unsupported operation '{op}'. Choose add, sub, mul, div")
    return ops[op](a, b)

if __name__ == "__main__":
    result = parse_and_run(sys.argv)
    # Print integers without .0 when appropriate, else print float
    if isinstance(result, float) and result.is_integer():
        print(int(result))
    else:
        print(result)
