class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children or []

    def _pretty(self, level=0):
        indent = "  " * level
        text = f"{indent}{self.node_type}: {self.value}\n"
        for child in self.children:
            text += child._pretty(level + 1)
        return text

    def __repr__(self):
        return self._pretty()