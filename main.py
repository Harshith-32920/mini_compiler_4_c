# from parser import tokenize, infix_to_ast, Node
# from semantic import SemanticAnalyzer
# from icg import IntermediateCodeGenerator

# print("Enter multiple expressions (type 'exit' to stop):\n")

# while True:
#     expr = input(">>> ")

#     if expr.lower() == "exit":
#         break

#     try:
#         # -------- Assignment Handling -------- #
#         if "<-" in expr:
#             left, right = expr.split("<-")
#             left = left.strip()
#             right = right.strip()

#             tokens = tokenize(right)
#             ast = infix_to_ast(tokens)

#             ast = Node("<-", Node(left), ast)

#         else:
#             tokens = tokenize(expr)
#             ast = infix_to_ast(tokens)

#         # -------- Semantic -------- #
#         sem = SemanticAnalyzer()
#         # Declare variables dynamically (simple approach)
#         for token in tokens:
#             if token.isidentifier():
#                 sem.declare(token)
#         if "<-" in expr:
#             sem.declare(left)

#         sem.check(ast)

#         # -------- ICG -------- #
#         icg = IntermediateCodeGenerator()
#         icg.generate(ast)

#         icg.print_table()

#     except Exception as e:
#         print("Error:", e)



from parser import tokenize, infix_to_ast, Node
from semantic import SemanticAnalyzer
from icg import IntermediateCodeGenerator
from optimizer import CodeOptimizer

def process_expression(expr):
    print("\nINPUT:", expr)

    # ---------------- PARSER + ASSIGNMENT FIX ---------------- #
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

    # ---------------- SEMANTIC ---------------- #
    sem = SemanticAnalyzer()

    # Declare variables dynamically
    for t in tokens:
        if t.isidentifier():
            sem.declare(t)

    if "<-" in expr:
        sem.declare(left)

    sem.check(ast)

    # ---------------- ICG ---------------- #
    icg = IntermediateCodeGenerator()
    icg.generate(ast)

    print("\n--- ORIGINAL TAC ---")
    icg.print_table()

    # ---------------- OPTIMIZER ---------------- #
    optimizer = CodeOptimizer(icg.get_code())
    optimizer.optimize()

    print("\n--- OPTIMIZED TAC ---")
    optimizer.print_code()

    # ---------------- PASS TO CODEGEN ---------------- #
    optimized_code = optimizer.code

    return optimized_code


# ---------------- MAIN LOOP ---------------- #
if __name__ == "__main__":
    print("Enter expressions (type 'exit' to stop):")

    while True:
        expr = input(">>> ")

        if expr.lower() == "exit":
            break

        try:
            optimized_code = process_expression(expr)

            # Later: pass this to codegen
            # from codegen import generate_code
            # generate_code(optimized_code)

        except Exception as e:
            print("Error:", e)