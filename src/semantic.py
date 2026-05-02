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


def analyze(ast, symtab):
    if ast.node_type == "Program":
        for s in ast.children:
            analyze(s, symtab)

    elif ast.node_type == "VarDecl":
        t = analyze(ast.children[0], symtab)
        symtab.declare(ast.value, t)

    elif ast.node_type == "Assign":
        vt = symtab.lookup(ast.value)
        et = analyze(ast.children[0], symtab)
        if vt != et:
            raise Exception(f"Type Error: cannot assign {et} to {vt}")

    elif ast.node_type in ("If", "IfElse", "ForLoop"):
        analyze(ast.children[0], symtab)
        analyze(ast.children[1], symtab)
        if len(ast.children) == 3:
            analyze(ast.children[2], symtab)

    elif ast.node_type == "Switch":
        analyze(ast.children[0], symtab)
        for case in ast.children[1].children:
            analyze(case, symtab)

    elif ast.node_type in ("Case", "DefaultCase"):
        for c in ast.children:
            analyze(c, symtab)

    elif ast.node_type == "Block":
        symtab.enter_scope()
        for s in ast.children:
            analyze(s, symtab)
        symtab.exit_scope()

    elif ast.node_type == "BinaryOp":
        l = analyze(ast.children[0], symtab)
        r = analyze(ast.children[1], symtab)
        if l != r:
            raise Exception(f"Type Error: {l} and {r} mismatch")
        return "bool" if ast.value in ("<", ">", "==") else l

    elif ast.node_type == "Literal":
        return "int" if isinstance(ast.value, int) else symtab.lookup(ast.value)

    elif ast.node_type == "Return":
        return analyze(ast.children[0], symtab)