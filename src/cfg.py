class BasicBlock:
    _id = 0

    def __init__(self, label=""):
        self.id = BasicBlock._id
        BasicBlock._id += 1
        self.label = label
        self.statements = []
        self.next_blocks = []

    def connect(self, block):
        self.next_blocks.append(block)

    def __repr__(self):
        return f"Block {self.id}"


class CFG:
    def __init__(self):
        self.entry = BasicBlock("ENTRY")
        self.exit = BasicBlock("EXIT")
        self.blocks = [self.entry, self.exit]


def build_cfg(ast):
    cfg = CFG()
    current = cfg.entry

    for stmt in ast.children:
        current = process_statement(stmt, current, cfg)

    current.connect(cfg.exit)
    return cfg


def process_statement(stmt, current, cfg):

    # -------- SIMPLE --------
    if stmt.node_type in ["VarDecl", "Assign", "Return"]:
        block = BasicBlock(stmt.node_type)
        block.statements.append(stmt)
        cfg.blocks.append(block)

        current.connect(block)

        if stmt.node_type == "Return":
            block.connect(cfg.exit)
            return block

        return block

    # -------- IF --------
    elif stmt.node_type == "If":
        cond = BasicBlock("IF_COND")
        cond.statements.append(stmt.children[0])
        cfg.blocks.append(cond)

        current.connect(cond)

        then_end = process_block(stmt.children[1], cond, cfg)

        merge = BasicBlock("MERGE")
        cfg.blocks.append(merge)

        cond.connect(merge)
        then_end.connect(merge)

        return merge

    # -------- IF ELSE --------
    elif stmt.node_type == "IfElse":
        cond = BasicBlock("IF_COND")
        cond.statements.append(stmt.children[0])
        cfg.blocks.append(cond)

        current.connect(cond)

        then_end = process_block(stmt.children[1], cond, cfg)
        else_end = process_block(stmt.children[2], cond, cfg)

        merge = BasicBlock("MERGE")
        cfg.blocks.append(merge)

        then_end.connect(merge)
        else_end.connect(merge)

        return merge

    # -------- FOR LOOP --------
    elif stmt.node_type == "ForLoop":
        cond = BasicBlock("LOOP_COND")
        cond.statements.append(stmt.children[0])
        cfg.blocks.append(cond)

        current.connect(cond)

        body_end = process_block(stmt.children[1], cond, cfg)
        body_end.connect(cond)  # loop back

        after = BasicBlock("AFTER_LOOP")
        cfg.blocks.append(after)

        cond.connect(after)
        return after

    # -------- SWITCH --------
    elif stmt.node_type == "Switch":
        switch_block = BasicBlock("SWITCH")
        switch_block.statements.append(stmt.children[0])
        cfg.blocks.append(switch_block)

        current.connect(switch_block)

        merge = BasicBlock("SWITCH_MERGE")
        cfg.blocks.append(merge)

        for case in stmt.children[1].children:
            case_block = BasicBlock("CASE")
            cfg.blocks.append(case_block)

            switch_block.connect(case_block)

            end = process_block(case.children[-1], case_block, cfg)
            end.connect(merge)

        return merge

    # -------- BLOCK --------
    elif stmt.node_type == "Block":
        return process_block(stmt, current, cfg)

    return current


def process_block(block_node, current, cfg):
    for stmt in block_node.children:
        current = process_statement(stmt, current, cfg)
    return current