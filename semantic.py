class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    # Simulate variable declaration (like: int a;)
    def declare(self, var):
        self.symbol_table[var] = True

    def check(self, node):
        if node is None:
            return

        # Variable check
        if node.value.isidentifier():
            if node.value not in self.symbol_table:
                raise Exception(f"Semantic Error: Undeclared variable '{node.value}'")

        # Operator check
        if node.value in ['+', '-', '*', '/']:
            if not node.left or not node.right:
                raise Exception("Semantic Error: Operator missing operands")

        self.check(node.left)
        self.check(node.right)