import sys
from parser import parse_code
from semantic import SymbolTable

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

    elif ast.node_type in ("If","IfElse","ForLoop"):
        analyze(ast.children[0], symtab)
        analyze(ast.children[1], symtab)
        if len(ast.children) == 3:
            analyze(ast.children[2], symtab)

    elif ast.node_type == "Switch":
        analyze(ast.children[0], symtab)        # switch expression
        cases_node = ast.children[1]            # Cases node
        for case in cases_node.children:
            analyze(case, symtab)

    elif ast.node_type in ("Case","DefaultCase"):
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
        return "bool" if ast.value in ("<",">","==") else l

    elif ast.node_type == "Literal":
        return "int" if isinstance(ast.value, int) else symtab.lookup(ast.value)

    elif ast.node_type == "Return":
        return analyze(ast.children[0], symtab)


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <file.go> [--ast | --check]")
        return

    filename = sys.argv[1]
    flag = sys.argv[2] if len(sys.argv) == 3 else "--ast"

    with open(filename) as f:
        code = f.read()

    try:
        ast = parse_code(code)
        symtab = SymbolTable()
        analyze(ast, symtab)

        print("✅ Syntax + Semantic + Type Checking Passed")

        if flag == "--ast":
            print("\n🌳 AST:\n")
            print(ast)

    except Exception as e:
        print("\n❌ Error:")
        print(e)

if __name__ == "__main__":
    main()