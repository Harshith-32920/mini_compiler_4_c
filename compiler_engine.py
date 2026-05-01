from parser import infix_to_ast, Node
from semantic import SemanticAnalyzer
from icg import IntermediateCodeGenerator
from optimizer import CodeOptimizer
from lex import lexical_analyzer
from codegen import CodeGenerator
import io
import sys

def compile_xlang(expr):
    results = {}
    try:
        # ---------------- LEXER ---------------- #
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

        results['lexer'] = full_tokens # List of (kind, value, pos)

        # ---------------- PARSER (AST) ---------------- #
        # Capture the AST display output
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        ast.display()
        sys.stdout = old_stdout
        results['ast'] = new_stdout.getvalue()

        # ---------------- SEMANTIC ---------------- #
        sem = SemanticAnalyzer()
        for t in tokens:
            if t.isidentifier():
                sem.declare(t)
        if "<-" in expr:
            sem.declare(left)
        
        sem.check(ast)
        results['semantic'] = "Validation Successful: No errors found."

        # ---------------- ICG ---------------- #
        icg = IntermediateCodeGenerator()
        icg.generate(ast)
        results['original_tac'] = icg.get_code()

        # ---------------- OPTIMIZER ---------------- #
        optimizer = CodeOptimizer(icg.get_code())
        optimizer.optimize()
        results['optimized_tac'] = optimizer.code

        # ---------------- CODEGEN ---------------- #
        cg = CodeGenerator(optimizer.code)
        cg.generate()
        results['assembly'] = [line for line in cg.target_code if line.strip()]

        results['success'] = True
    except Exception as e:
        results['success'] = False
        results['error'] = str(e)
    
    return results
