temp_counter = 1
intermediate_code = []

def new_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def generate_ic(node):
    if node[0] == 'decl':
        var_name = node[1]
        value = node[2]
        if isinstance(value, tuple):
            result = generate_ic(value)
            intermediate_code.append(f"{var_name} = {result}")
        else:
            intermediate_code.append(f"{var_name} = {value}")
    
    elif node[0] == 'assign':
        var_name = node[1]
        value = node[2]
        if isinstance(value, tuple):
            result = generate_ic(value)
            intermediate_code.append(f"{var_name} = {result}")
        else:
            intermediate_code.append(f"{var_name} = {value}")

    elif node[0] == 'op':
        op = node[1]
        left = node[2]
        right = node[3]

        if isinstance(left, tuple):
            left = generate_ic(left)
        if isinstance(right, tuple):
            right = generate_ic(right)

        temp = new_temp()
        intermediate_code.append(f"{temp} = {left} {op} {right}")
        return temp

    elif node[0] == 'print':
        intermediate_code.append(f"print {node[1]}")

def generate_code(ast):
    global intermediate_code, temp_counter
    intermediate_code = []
    temp_counter = 1
    for node in ast:
        generate_ic(node)
    return intermediate_code

# Example usage
if __name__ == "__main__":
    from parser import parser

    data = '''
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    '''

    ast = parser.parse(data)
    tac = generate_code(ast)

    for line in tac:
        print(line)
