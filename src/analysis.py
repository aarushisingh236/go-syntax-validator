def get_reachable_blocks(cfg):
    visited = set()

    def dfs(block):
        if block in visited:
            return
        visited.add(block)
        for nxt in block.next_blocks:
            dfs(nxt)

    dfs(cfg.entry)
    return visited


def detect_dead_code(cfg):
    reachable = get_reachable_blocks(cfg)
    dead = [b for b in cfg.blocks if b not in reachable]
    return dead


def collect_variable_usage(ast):
    declared = set()
    used = set()

    def walk(node):
        if node.node_type == "VarDecl":
            declared.add(node.value)
        elif node.node_type == "Assign":
            used.add(node.value)
        elif node.node_type == "Literal":
            if isinstance(node.value, str):
                used.add(node.value)

        for c in node.children:
            walk(c)

    walk(ast)
    return declared, used


def detect_unused_variables(ast):
    declared, used = collect_variable_usage(ast)
    return declared - used