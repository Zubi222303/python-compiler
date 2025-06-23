import re

class Optimizer:
    def __init__(self, tac_instructions):
        self.original = tac_instructions
        self.optimized = []

    def is_constant(self, value):
        return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None

    def fold_constants_and_propagate(self):
        temp_values = {}     # Track values of temporaries
        variable_values = {} # Track values of named variables

        new_code = []

        for instr in self.original:
            parts = instr.strip().split()

            if not parts:
                continue

            # Handle arithmetic ops
            if len(parts) == 4 and parts[0] in {'ADD', 'SUB', 'MUL', 'DIV'}:
                op, a, b, result = parts
                a_val = temp_values.get(a, variable_values.get(a, a))
                b_val = temp_values.get(b, variable_values.get(b, b))

                if self.is_constant(a_val) and self.is_constant(b_val):
                    a_num = float(a_val)
                    b_num = float(b_val)
                    res = None
                    if op == 'ADD': res = a_num + b_num
                    elif op == 'SUB': res = a_num - b_num
                    elif op == 'MUL': res = a_num * b_num
                    elif op == 'DIV': res = a_num / b_num if b_num != 0 else 0

                    res = int(res) if res.is_integer() else res
                    temp_values[result] = str(res)
                    new_code.append(f"LOAD {res} {result}")
                else:
                    temp_values[result] = result
                    new_code.append(instr)

            # Handle LOAD
            elif len(parts) == 3 and parts[0] == 'LOAD':
                _, value, target = parts
                const_val = temp_values.get(value, variable_values.get(value, value))
                if self.is_constant(const_val):
                    variable_values[target] = const_val
                else:
                    variable_values.pop(target, None)
                new_code.append(f"LOAD {const_val} {target}")

            # Handle STORE
            elif len(parts) == 3 and parts[0] == 'STORE':
                _, source, target = parts
                value = temp_values.get(source, variable_values.get(source, source))
                if self.is_constant(value):
                    variable_values[target] = value
                    new_code.append(f"LOAD {value} {target}")
                else:
                    variable_values.pop(target, None)
                    new_code.append(f"STORE {value} {target}")

            # Handle PRINT
            elif len(parts) == 2 and parts[0] == 'PRINT':
                val = temp_values.get(parts[1], variable_values.get(parts[1], parts[1]))
                new_code.append(f"PRINT {val}")

            else:
                new_code.append(instr)

        self.optimized = new_code

    def eliminate_dead_code(self):
        used_vars = set()
        final_code = []

        for instr in reversed(self.optimized):
            parts = instr.strip().split()

            if not parts:
                continue

            if parts[0] == "PRINT":
                used_vars.add(parts[1])
                final_code.insert(0, instr)

            elif parts[0] == "LOAD" and len(parts) == 3:
                val, var = parts[1], parts[2]
                if var in used_vars:
                    final_code.insert(0, instr)
                    if not self.is_constant(val):
                        used_vars.add(val)

            elif parts[0] == "STORE" and len(parts) == 3:
                val, var = parts[1], parts[2]
                if var in used_vars:
                    final_code.insert(0, instr)
                    used_vars.add(val)

            elif len(parts) == 4 and parts[0] in {"ADD", "SUB", "MUL", "DIV"}:
                op, a, b, res = parts
                if res in used_vars or res.startswith("t"):
                    final_code.insert(0, instr)
                    used_vars.update([a, b])

            else:
                final_code.insert(0, instr)

        self.optimized = final_code

    def optimize(self):
        self.fold_constants_and_propagate()
        self.eliminate_dead_code()
        return self.optimized
