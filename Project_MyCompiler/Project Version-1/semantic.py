class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, var_name, var_value):
        if var_name in self.symbols:
            raise Exception(f"Variable '{var_name}' is already declared.")
        self.symbols[var_name] = var_value

    def lookup(self, var_name):
        if var_name not in self.symbols:
            raise Exception(f"Variable '{var_name}' is not declared.")
        return self.symbols[var_name]
