class SymbolTable:
    def __init__(self):
        self.table = {}

    def add(self, name, value=None):
        if name in self.table:
            print(f"Warning: Variable '{name}' already declared.")
        self.table[name] = {"value": value}

    def update(self, name, value):
        if name in self.table:
            self.table[name]["value"] = value
        else:
            raise NameError(f"Variable '{name}' not declared.")

    def get(self, name):
        if name in self.table:
            return self.table[name]
        else:
            raise NameError(f"Variable '{name}' not declared.")

    def display(self):
        print("\nSymbol Table:")
        for name, info in self.table.items():
            print(f"{name}: {info}")
