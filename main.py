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



from parser import infix_to_ast, Node
from semantic import SemanticAnalyzer
from icg import IntermediateCodeGenerator
from optimizer import CodeOptimizer
from lex import lexical_analyzer, print_table as print_lex_table

def process_expression(expr):
    print("\nINPUT:", expr)

    # ---------------- PARSER + ASSIGNMENT FIX ---------------- #
    if "<-" in expr:
        left, right = expr.split("<-")
        left = left.strip()
        right = right.strip()

        full_tokens = lexical_analyzer(right)
        tokens = [t[1] for t in full_tokens]
        ast = infix_to_ast(tokens)

        ast = Node("<-", Node(left), ast)
    else:
        full_tokens = lexical_analyzer(expr)
        tokens = [t[1] for t in full_tokens]
        ast = infix_to_ast(tokens)

    # ---------------- LEXER OUTPUT ---------------- #
    print_lex_table(full_tokens)

    # ---------------- PARSER OUTPUT (AST) ---------------- #
    print("\n--- PARSER OUTPUT (AST) ---")
    ast.display()

    # ---------------- SEMANTIC ---------------- #
    sem = SemanticAnalyzer()

    # Declare variables dynamically
    for t in tokens:
        if t.isidentifier():
            sem.declare(t)

    if "<-" in expr:
        sem.declare(left)

    sem.check(ast)
    print("\n--- SEMANTIC ANALYSIS ---")
    print("Validation Successful: No errors found.")

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

    from codegen import generate_code
    generate_code(optimized_code)

    return optimized_code


# ---------------- MAIN LOOP ---------------- #
if __name__ == "__main__":
    print("Enter expressions (type 'exit' to stop):")

    while True:
        expr = input(">>> ")

        if expr.lower() == "exit":
            break

        try:
            process_expression(expr)
        except Exception as e:
            print("Error:", e)