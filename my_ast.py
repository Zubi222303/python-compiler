class ASTNode:
    def __init__(self, node_type, children=None, value=None, line=None, column=None):
        self.type = node_type
        self.children = children or []
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self, level=0):
        ret = "  " * level + f"{self.type}"
        if self.value is not None:
            ret += f": {self.value}"
        if self.line is not None:
            ret += f" (Line: {self.line}, Column: {self.column})"
        ret += "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret