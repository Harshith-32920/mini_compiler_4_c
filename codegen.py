class CodeGenerator:
    def __init__(self, optimized_code):
        self.code = optimized_code
        self.target_code = []

    def generate(self):
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV'
        }

        for line in self.code:
            # line is like "t1 = a + b" or "x = t1" or "t1 = 5"
            if "=" not in line:
                continue
                
            left, right = map(str.strip, line.split("="))
            parts = right.split()

            if len(parts) == 3:
                # Binary operation: a op b
                a, op, b = parts
                self.target_code.append(f"LOAD {a}")
                asm_op = op_map.get(op, "OP")
                self.target_code.append(f"{asm_op} {b}")
                self.target_code.append(f"STORE {left}")
            elif len(parts) == 1:
                # Direct assignment: a
                val = parts[0]
                self.target_code.append(f"LOAD {val}")
                self.target_code.append(f"STORE {left}")
            
            self.target_code.append("") # Blank line for readability

    def print_code(self):
        print("\n--- TARGET CODE (PSEUDO ASSEMBLY) ---")
        print(f"{'Step':<10}{'Instruction'}")
        print("-" * 45)
        step = 1
        for line in self.target_code:
            if line.strip():
                print(f"{step:<10}{line}")
                step += 1
            else:
                print("")

def generate_code(optimized_code):
    cg = CodeGenerator(optimized_code)
    cg.generate()
    cg.print_code()
