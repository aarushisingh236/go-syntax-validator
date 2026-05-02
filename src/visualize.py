import networkx as nx
import matplotlib.pyplot as plt


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


# ---------- CFG Visualization ----------
def visualize_cfg(cfg):
    G = nx.DiGraph()

    labels = {}
    node_colors = []

    for block in cfg.blocks:
        label = f"B{block.id}\n{block.label}"

        if block.statements:
            for stmt in block.statements:
                label += "\n" + format_stmt(stmt)
        else:
            label += "\n[Empty]"

        G.add_node(block.id)
        labels[block.id] = label

        # 🎨 Color coding
        if block.label in ["ENTRY", "EXIT"]:
            node_colors.append("lightgreen")
        elif "COND" in block.label:
            node_colors.append("orange")
        elif "SWITCH" in block.label:
            node_colors.append("violet")
        elif "MERGE" in block.label:
            node_colors.append("gray")
        else:
            node_colors.append("skyblue")

        for nxt in block.next_blocks:
            G.add_edge(block.id, nxt.id)

    # 🔥 FINAL TUNED LAYOUT (balanced + centered)
    pos = nx.spring_layout(
        G,
        k=1.2,          # tighter clustering
        iterations=200,
        seed=42,
        scale=2,
        center=(0, 0)
    )

    # Normalize positions (prevents extreme spread)
    for node in pos:
        pos[node] = (pos[node][0] * 2, pos[node][1] * 2)

    plt.figure(figsize=(12, 9))

    nx.draw(
        G,
        pos,
        labels=labels,
        node_color=node_colors,
        with_labels=True,
        node_size=3000,
        font_size=9,
        arrows=True,
        edge_color="black"
    )

    plt.title("Control Flow Graph (CFG)", fontsize=14)
    plt.tight_layout()
    plt.show()


# ---------- AST Visualization ----------
def visualize_ast(ast):
    G = nx.DiGraph()

    def add(node, parent=None):
        node_id = id(node)

        label = node.node_type
        if node.value is not None:
            label += f":{node.value}"

        G.add_node(node_id, label=label)

        if parent:
            G.add_edge(parent, node_id)

        for c in node.children:
            add(c, node_id)

    add(ast)

    labels = nx.get_node_attributes(G, 'label')

    # Balanced layout for tree
    pos = nx.spring_layout(
        G,
        k=1.3,
        iterations=200,
        seed=42
    )

    plt.figure(figsize=(12, 9))

    nx.draw(
        G,
        pos,
        labels=labels,
        with_labels=True,
        node_size=2500,
        font_size=8
    )

    plt.title("AST Visualization", fontsize=14)
    plt.tight_layout()
    plt.show()