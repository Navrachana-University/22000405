def run_simulator(assembly_code):
    variables = {}
    labels = {}
    pc = 0

    # First pass to gather labels
    for i, line in enumerate(assembly_code):
        line = line.strip()
        if line.endswith(':'):
            label_name = line[:-1]
            labels[label_name] = i

    # Second pass to run instructions
    while pc < len(assembly_code):
        line = assembly_code[pc].strip()
        if not line or line.endswith(':'):
            pc += 1
            continue

        parts = [part.strip(',') for part in line.split()]

        if parts[0] == 'MOV':
            var = parts[1]
            value = parts[2]
            if value.isdigit():
                variables[var] = int(value)
            elif value in variables:
                variables[var] = variables[value]
            else:
                print(f"[ERROR] Undefined variable or invalid value: {value}")
                return

        elif parts[0] == 'CMP':
            left = parts[1]
            right = parts[2]
            try:
                cmp_left = variables.get(left, int(left) if left.isdigit() else None)
                cmp_right = variables.get(right, int(right) if right.isdigit() else None)

                if cmp_left is None or cmp_right is None:
                    raise ValueError("Invalid operand(s) for CMP")

                variables['cmp_left'] = cmp_left
                variables['cmp_right'] = cmp_right
                variables['cmp_result'] = 1 if cmp_left < cmp_right else 0
            except ValueError as e:
                print(f"[ERROR] {e}: {left} or {right}")
                return

        elif parts[0] == 'SETL':
            var = parts[1]
            variables[var] = variables.get('cmp_result', 0)

        elif parts[0] == 'JZ':
            condition = parts[1]
            label = parts[2]
            if variables.get(condition, 0) == 0:
                if label in labels:
                    pc = labels[label]
                    continue
                else:
                    print(f"[ERROR] Label not found: {label}")
                    return

        elif parts[0] == 'JMP':
            label = parts[1]
            if label in labels:
                pc = labels[label]
                continue
            else:
                print(f"[ERROR] Label not found: {label}")
                return

        elif parts[0] == 'PRINT':
            var = parts[1]
            print(f"{var}: {variables.get(var, 'undefined')}")

        pc += 1


if __name__ == "__main__":
    try:
        with open("output.asm", "r") as f:
            assembly_code = f.readlines()
            run_simulator(assembly_code)
    except FileNotFoundError:
        print("output.asm not found. Please generate it first.")
