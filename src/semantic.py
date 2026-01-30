class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, var_type):
        if name in self.scopes[-1]:
            raise Exception(f"Semantic Error: '{name}' redeclared")
        self.scopes[-1][name] = var_type

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Semantic Error: '{name}' not declared")