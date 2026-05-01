class CodeOptimizer:
    def __init__(self, code):
        self.code = code

    # ---------------- UTIL ---------------- #
    def is_number(self, x):
        return x.isdigit()

    # ---------------- 1. CONSTANT FOLDING ---------------- #
    def constant_folding(self):
        new_code = []

        for line in self.code:
            left, right = map(str.strip, line.split("="))
            tokens = right.split()

            if len(tokens) == 3:
                a, op, b = tokens

                if self.is_number(a) and self.is_number(b):
                    a, b = int(a), int(b)

                    if op == '+': val = a + b
                    elif op == '-': val = a - b
                    elif op == '*': val = a * b
                    elif op == '/': val = a // b if b != 0 else 0
                    else: val = None

                    if val is not None:
                        new_code.append(f"{left} = {val}")
                        continue

            new_code.append(line)

        self.code = new_code

    # ---------------- 2. CONSTANT PROPAGATION ---------------- #
    def constant_propagation(self):
        constants = {}
        new_code = []

        for line in self.code:
            left, right = map(str.strip, line.split("="))
            tokens = right.split()

            # Replace known constants
            tokens = [str(constants.get(t, t)) for t in tokens]

            new_right = " ".join(tokens)

            # Store constant assignments
            if len(tokens) == 1 and self.is_number(tokens[0]):
                constants[left] = tokens[0]

            new_code.append(f"{left} = {new_right}")

        self.code = new_code

    # ---------------- 3. COPY PROPAGATION ---------------- #
    def copy_propagation(self):
        copies = {}
        new_code = []

        for line in self.code:
            left, right = map(str.strip, line.split("="))
            tokens = right.split()

            tokens = [copies.get(t, t) for t in tokens]

            if len(tokens) == 1 and tokens[0].startswith("t"):
                copies[left] = tokens[0]

            new_code.append(f"{left} = {' '.join(tokens)}")

        self.code = new_code

    # ---------------- 4. ALGEBRAIC SIMPLIFICATION ---------------- #
    def algebraic_simplification(self):
        new_code = []

        for line in self.code:
            left, right = map(str.strip, line.split("="))
            tokens = right.split()

            if len(tokens) == 3:
                a, op, b = tokens

                if op == '+' and b == '0':
                    new_code.append(f"{left} = {a}")
                    continue
                if op == '+' and a == '0':
                    new_code.append(f"{left} = {b}")
                    continue

                if op == '*' and b == '1':
                    new_code.append(f"{left} = {a}")
                    continue
                if op == '*' and a == '1':
                    new_code.append(f"{left} = {b}")
                    continue

                if op == '*' and (a == '0' or b == '0'):
                    new_code.append(f"{left} = 0")
                    continue

            new_code.append(line)

        self.code = new_code

    # ---------------- 5. COMMON SUBEXPRESSION ELIMINATION ---------------- #
    def common_subexpression_elimination(self):
        expr_map = {}
        new_code = []

        for line in self.code:
            left, right = map(str.strip, line.split("="))

            if right in expr_map:
                # Reuse previous computation
                new_code.append(f"{left} = {expr_map[right]}")
            else:
                expr_map[right] = left
                new_code.append(line)

        self.code = new_code

    # ---------------- 6. DEAD CODE ELIMINATION ---------------- #
    def dead_code_elimination(self):
        used = set()
        new_code = []

        # Find used variables
        for line in reversed(self.code):
            left, right = map(str.strip, line.split("="))
            tokens = right.split()

            # Keep if it's a user variable (not starting with 't') or if it's a used temp
            if not left.startswith("t") or left in used:
                new_code.append(line)
                used.update(tokens)

        self.code = list(reversed(new_code))

    # ---------------- RUN ALL OPTIMIZATIONS ---------------- #
    def optimize(self):
        self.constant_folding()
        self.constant_propagation()
        self.copy_propagation()
        self.algebraic_simplification()
        self.common_subexpression_elimination()
        self.dead_code_elimination()

    # ---------------- PRINT ---------------- #
    def print_code(self):
        print("\nOPTIMIZED INTERMEDIATE CODE\n")
        print(f"{'Step':<10}{'Instruction'}")
        print("-" * 45)

        for i, line in enumerate(self.code, 1):
            print(f"{i:<10}{line}")