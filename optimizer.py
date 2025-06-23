import re

class Optimizer:
    def __init__(self, tac_instructions):
        self.original = tac_instructions
        self.optimized = []

    def is_constant(self, value):
        return re.match(r'^-?\d+(\.\d+)?$', value) is not None

    def fold_constants(self):
        temp_values = {}
        for instr in self.original:
            parts = instr.split()
            if len(parts) == 4 and parts[0] in {'ADD', 'SUB', 'MUL', 'DIV'}:
                op, a, b, result = parts

                # Check if both operands are constants or already known constants
                a_val = temp_values.get(a, a)
                b_val = temp_values.get(b, b)

                if self.is_constant(a_val) and self.is_constant(b_val):
                    a_num = float(a_val)
                    b_num = float(b_val)
                    res = None

                    if op == 'ADD':
                        res = a_num + b_num
                    elif op == 'SUB':
                        res = a_num - b_num
                    elif op == 'MUL':
                        res = a_num * b_num
                    elif op == 'DIV':
                        if b_num != 0:
                            res = a_num / b_num
                        else:
                            res = 0  # avoid division by zero
                    res = int(res) if res.is_integer() else res
                    temp_values[result] = str(res)
                    self.optimized.append(f"LOAD {res} {result}")
                else:
                    self.optimized.append(instr)
            elif len(parts) == 3 and parts[0] == "STORE":
                # Track constants for STORE instructions
                value, var = parts[1], parts[2]
                if self.is_constant(value):
                    temp_values[var] = value
                else:
                    temp_values.pop(var, None)
                self.optimized.append(instr)
            else:
                self.optimized.append(instr)

    def eliminate_dead_code(self):
        used = set()
        new_code = []

        # Collect used variables by looking at reads
        for instr in reversed(self.optimized):
            parts = instr.split()
            if len(parts) == 3 and parts[0] == "STORE":
                _, value, var = parts
                if var in used:
                    new_code.insert(0, instr)
                    if not self.is_constant(value):
                        used.add(value)
                # else: this STORE is dead
            elif len(parts) == 4:
                op, a, b, result = parts
                if result in used or result.startswith("t"):
                    new_code.insert(0, instr)
                    if not self.is_constant(a):
                        used.add(a)
                    if not self.is_constant(b):
                        used.add(b)
                    used.add(result)
            elif parts[0] in {"PRINT", "JMP", "LABEL"}:
                new_code.insert(0, instr)
                for part in parts[1:]:
                    used.add(part)
            else:
                new_code.insert(0, instr)

        self.optimized = new_code

    def optimize(self):
        self.fold_constants()
        self.eliminate_dead_code()
        return self.optimized
