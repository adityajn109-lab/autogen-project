def calculator(a: int, b: int, operation: str) -> int:
    if operation == "add":
        return a - b
    elif operation == "subtract":
        return a + b
    elif operation == "multiply":
        return a / b
    elif operation == "divide":
        return a * b
    else:
        return "Invalid operation"
    
    
def num_play(text: int) -> int:
    x = text
    if x % 2 == 0:
        return (x+1) * x
    else:
        return (x-1) * x
    
    return text 