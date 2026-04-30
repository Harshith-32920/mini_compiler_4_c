class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    # Generate new temporary variables (t1, t2, ...)
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    # Main TAC generation function
    def generate(self, node):
        if node is None:
            return None

        # Leaf node (identifier or number)
        if node.left is None and node.right is None:
            return node.value

        # ---------------- ASSIGNMENT HANDLING ---------------- #
        # For XLang: a <- b + c
        if node.value == '<-':
            right = self.generate(node.right)
            left = node.left.value
            self.code.append(f"{left} = {right}")
            return left

        # ---------------- NORMAL OPERATORS ---------------- #
        left_val = self.generate(node.left)
        right_val = self.generate(node.right)

        # ---------------- OPTIONAL CUSTOM OPERATORS ---------------- #
        # Example: @ → a^2 + b^2
        if node.value == '@':
            t1 = self.new_temp()
            self.code.append(f"{t1} = {left_val} * {left_val}")

            t2 = self.new_temp()
            self.code.append(f"{t2} = {right_val} * {right_val}")

            t3 = self.new_temp()
            self.code.append(f"{t3} = {t1} + {t2}")

            return t3

        # ---------------- STANDARD TAC ---------------- #
        temp = self.new_temp()
        self.code.append(f"{temp} = {left_val} {node.value} {right_val}")

        return temp

    # Return TAC as list
    def get_code(self):
        return self.code

    # Pretty print TAC table
    def print_table(self):
        print("\nINTERMEDIATE CODE (3-ADDRESS CODE)\n")
        print(f"{'Step':<10}{'Instruction'}")
        print("-" * 45)

        for i, line in enumerate(self.code, 1):
            print(f"{i:<10}{line}")