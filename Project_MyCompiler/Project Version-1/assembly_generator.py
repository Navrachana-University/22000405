def tac_to_assembly(tac):
    asm = []
    label_counter = 0
    while_counter = 0

    def clean_assembly_line(line):
        """Remove unwanted characters like colons from assembly lines."""
        line = line.strip()  # Remove leading/trailing spaces
        line = line.replace(":", "")  # Remove colons
        return line

    for line in tac:
        if line.startswith("chhapo"):
            parts = line.split()
            asm.append(f"PRINT {parts[1]}")
        elif line.startswith("agar"):
            parts = line.split()
            asm.append(f"CMP {parts[1]}, 0")
            asm.append(f"JZ {parts[1]}, ELSE{label_counter}")
        elif line.startswith("warna:"):
            asm.append(f"JMP ENDIF{label_counter}")
            asm.append(f"ENDIF{label_counter}:")
            label_counter += 1
        elif line.startswith("jabtak"):
            parts = line.split()
            asm.append(f"WHILE{while_counter}:")
            asm.append(f"CMP {parts[1]}, 0")
            asm.append(f"SETL {parts[1]}")
            asm.append(f"JZ {parts[1]}, ENDWHILE{while_counter}")
        elif line.startswith("t") and '=' in line and any(op in line for op in ['+', '-', '*', '/','<']):
            parts = line.split('=')
            dest = parts[0].strip()
            expr = parts[1].strip()
            op_parts = expr.split()
            left = op_parts[0]
            op = op_parts[1]
            right = op_parts[2]
            asm.append(f"MOV R1, {left}")
            if op == '+':
                asm.append(f"ADD R1, {right}")
            elif op == '-':
                asm.append(f"SUB R1, {right}")
            elif op == '*':
                asm.append(f"MUL R1, {right}")
            elif op == '/':
                asm.append(f"DIV R1, {right}")
            elif op == '<':
                asm.append(f"CMP {left}, {right}")
                asm.append(f"SETL {dest}")
                continue
            asm.append(f"MOV {dest}, R1")
        elif '=' in line:
            lhs, rhs = line.split('=')
            asm.append(f"MOV {lhs.strip()}, {rhs.strip()}")
        elif line.startswith("chhapo"):
            parts = line.split()
            asm.append(f"PRINT {parts[1]}")
        elif line.startswith("ENDIF") or line.startswith("ENDWHILE"):
            asm.append(line + ":")
        elif line.startswith("JMP") or line.startswith("JZ") or line.startswith("SETL") or line.startswith("CMP"):
            asm.append(line)
        elif line.startswith("a = t"):
            # Direct variable assignment from temp
            lhs, rhs = line.split('=')
            asm.append(f"MOV {lhs.strip()}, {rhs.strip()}")
        elif line.startswith("t"):
            # Temp assignment from expr
            parts = line.split('=')
            dest = parts[0].strip()
            expr = parts[1].strip()
            asm.append(f"MOV {dest}, {expr}")

    # Clean the assembly code before returning it
    asm = [clean_assembly_line(line) for line in asm]

    return asm
