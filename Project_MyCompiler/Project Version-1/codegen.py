class CodeGenerator:
    def __init__(self):
        self.symbol_table = {}
        self.three_address_code = []

    def generate(self, ast):
        code = []
        for node in ast:
            if node[0] == 'decl':
                self.declare_variable(node, code)
            elif node[0] == 'assign':
                self.assign_value(node, code)
            elif node[0] == 'print':
                self.print_value(node, code)
            elif node[0] == 'if-else':
                self.if_else(node, code)
            elif node[0] == 'while':
                self.while_loop(node, code)

        # Perform optimizations
        code = self.constant_folding(code)  # Apply constant folding
        code = self.dead_code_elimination(code)  # Apply dead code elimination
        
        # Store optimized code
        self.three_address_code = code

        # Write to output.asm file
        with open('output.asm', 'w') as f:
            for line in code:
                f.write(line + '\n')


    def declare_variable(self, node, code):
        var_name = node[1]
        value = node[2]
        # Add the variable to the symbol table
        self.symbol_table[var_name] = value
        # Generate the declaration code
        code.append(f"{var_name} = {value}")

    def assign_value(self, node, code):
        var_name = node[1]
        value = self.generate_expression(node[2])  # Assuming `generate_expression` handles expressions
        code.append(f"{var_name} = {value}")

    def print_value(self, node, code):
        var_name = node[1]
        code.append(f"print {var_name}")

    def if_else(self, node, code):
        condition = self.generate_expression(node[1])
        true_branch = node[2]
        false_branch = node[3]
        
        # Add conditional code (simplified for demonstration)
        code.append(f"if {condition}:")
        self.generate(true_branch)  # Generate code for the true branch
        code.append("else:")
        self.generate(false_branch)  # Generate code for the false branch

    def while_loop(self, node, code):
        condition = self.generate_expression(node[1])
        body = node[2]
        
        # Add while loop code (simplified for demonstration)
        code.append(f"while {condition}:")
        self.generate(body)  # Generate code for the while loop body

    def generate_expression(self, expr):
        # This method would generate the appropriate expression (simplified for demonstration)
        if isinstance(expr, tuple):
            return f"({expr[1]} {expr[0]} {expr[2]})"
        return str(expr)

    def constant_folding(self, code):
        # Apply constant folding logic here
        return code
    
    def dead_code_elimination(self, code):
        # Apply dead code elimination logic here
        return code

    def print_code(self):
        for line in self.three_address_code:
            print(line)
    
    def show_symbols(self):
        print("Symbol Table:")
        for var, value in self.symbol_table.items():
            print(f"{var}: {value}")
