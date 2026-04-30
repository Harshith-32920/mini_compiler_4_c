import re

# ---------------- TOKENIZER ---------------- #
def tokenize(expr):
    token_pattern = r'\d+|[a-zA-Z_]\w*|[\+\-\*/\(\)]'
    return re.findall(token_pattern, expr)


# ---------------- AST NODE ---------------- #
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def display(self):
        lines, *_ = self._build_tree()
        for line in lines:
            print(line)

    def _build_tree(self):
        # No child
        if self.left is None and self.right is None:
            line = str(self.value)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child
        if self.right is None:
            lines, n, p, x = self.left._build_tree()
            s = str(self.value)
            u = len(s)

            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "

            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child
        if self.left is None:
            lines, n, p, x = self.right._build_tree()
            s = str(self.value)
            u = len(s)

            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "

            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children
        left, n, p, x = self.left._build_tree()
        right, m, q, y = self.right._build_tree()
        s = str(self.value)
        u = len(s)

        first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
        second_line = x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "

        if p < q:
            left += [" " * n] * (q - p)
        elif q < p:
            right += [" " * m] * (p - q)

        zipped_lines = zip(left, right)
        lines = [l + u * " " + r for l, r in zipped_lines]

        return [first_line, second_line] + lines, n + m + u, max(p, q) + 2, n + u // 2


# ---------------- INFIX PARSER ---------------- #
def infix_to_ast(tokens):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    output = []
    ops = []

    def apply_op():
        if len(output) < 2:
            raise Exception("Syntax Error: Not enough operands")
        right = output.pop()
        left = output.pop()
        op = ops.pop()
        output.append(Node(op, left, right))

    for token in tokens:
        if token.isdigit() or token.isidentifier():
            output.append(Node(token))

        elif token in precedence:
            while ops and ops[-1] in precedence and precedence[ops[-1]] >= precedence[token]:
                apply_op()
            ops.append(token)

        elif token == '(':
            ops.append(token)

        elif token == ')':
            while ops and ops[-1] != '(':
                apply_op()
            if not ops:
                raise Exception("Syntax Error: Mismatched parentheses")
            ops.pop()

    while ops:
        if ops[-1] == '(':
            raise Exception("Syntax Error: Mismatched parentheses")
        apply_op()

    if len(output) != 1:
        raise Exception("Syntax Error: Invalid expression")

    return output[0]


# ---------------- PREFIX PARSER ---------------- #
def prefix_to_ast(tokens):
    stack = []

    for token in reversed(tokens):
        if token.isdigit() or token.isidentifier():
            stack.append(Node(token))
        else:
            if len(stack) < 2:
                raise Exception("Syntax Error in prefix expression")
            left = stack.pop()
            right = stack.pop()
            stack.append(Node(token, left, right))

    if len(stack) != 1:
        raise Exception("Syntax Error in prefix expression")

    return stack[0]


# ---------------- POSTFIX PARSER ---------------- #
def postfix_to_ast(tokens):
    stack = []

    for token in tokens:
        if token.isdigit() or token.isidentifier():
            stack.append(Node(token))
        else:
            if len(stack) < 2:
                raise Exception("Syntax Error in postfix expression")
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(token, left, right))

    if len(stack) != 1:
        raise Exception("Syntax Error in postfix expression")

    return stack[0]