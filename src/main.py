import sys
from parser import parse_code
from semantic import SymbolTable, analyze

from cfg import build_cfg
from analysis import detect_dead_code, detect_unused_variables
from visualize import visualize_cfg, visualize_ast


# ---------- Pretty formatting ----------
def format_stmt(stmt):
    if stmt.node_type == "BinaryOp":
        left = stmt.children[0].value
        right = stmt.children[1].value
        return f"({left} {stmt.value} {right})"

    elif stmt.node_type == "Assign":
        return f"{stmt.value} = ..."

    elif stmt.node_type == "VarDecl":
        return f"var {stmt.value}"

    elif stmt.node_type == "Literal":
        return str(stmt.value)

    return stmt.node_type


# ---------- PRINT CFG (FULL, NO SKIPPING) ----------
def print_cfg(cfg):
    for block in cfg.blocks:
        print(f"\nBlock {block.id} [{block.label}]:")

        if block.statements:
            for stmt in block.statements:
                print(f"  {format_stmt(stmt)}")
        else:
            print("  [Empty]")

        next_ids = [b.id for b in block.next_blocks]
        print(f"  → {next_ids}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <file.go> [--ast | --cfg | --viz-cfg | --viz-ast | --analyze]")
        return

    filename = sys.argv[1]
    flag = sys.argv[2] if len(sys.argv) >= 3 else "--ast"

    try:
        with open(filename) as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return

    try:
        # ---------- PARSE ----------
        ast = parse_code(code)

        # ---------- SEMANTIC ----------
        symtab = SymbolTable()
        analyze(ast, symtab)

        print("✅ Syntax + Semantic + Type Checking Passed")

        # ---------- CFG ----------
        cfg = build_cfg(ast)

        # ---------- FLAGS ----------
        if flag == "--ast":
            print("\n🌳 AST:\n")
            print(ast)

        elif flag == "--cfg":
            print("\n🔀 CFG Structure:")
            print_cfg(cfg)

        elif flag == "--viz-ast":
            visualize_ast(ast)

        elif flag == "--viz-cfg":
            visualize_cfg(cfg)

        elif flag == "--analyze":
            print("\n🔍 Static Analysis:\n")

            dead = detect_dead_code(cfg)
            unused = detect_unused_variables(ast)

            if dead:
                print("⚠️ Dead Code Blocks:")
                for b in dead:
                    print(f"  Block {b.id}")
            else:
                print("✅ No dead code")

            if unused:
                print("\n⚠️ Unused Variables:")
                for v in unused:
                    print(f"  {v}")
            else:
                print("✅ No unused variables")

        else:
            print("❌ Unknown flag")

    except Exception as e:
        print("\n❌ Error:")
        print(e)


if __name__ == "__main__":
    main()