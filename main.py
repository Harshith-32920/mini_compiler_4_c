from parser import tokenize, infix_to_ast, Node
from semantic import SemanticAnalyzer
from icg import IntermediateCodeGenerator

print("Enter multiple expressions (type 'exit' to stop):\n")

while True:
    expr = input(">>> ")

    if expr.lower() == "exit":
        break

    try:
        # -------- Assignment Handling -------- #
        if "<-" in expr:
            left, right = expr.split("<-")
            left = left.strip()
            right = right.strip()

            tokens = tokenize(right)
            ast = infix_to_ast(tokens)

            ast = Node("<-", Node(left), ast)

        else:
            tokens = tokenize(expr)
            ast = infix_to_ast(tokens)

        # -------- Semantic -------- #
        sem = SemanticAnalyzer()
        # Declare variables dynamically (simple approach)
        for token in tokens:
            if token.isidentifier():
                sem.declare(token)
        if "<-" in expr:
            sem.declare(left)

        sem.check(ast)

        # -------- ICG -------- #
        icg = IntermediateCodeGenerator()
        icg.generate(ast)

        icg.print_table()

    except Exception as e:
        print("Error:", e)