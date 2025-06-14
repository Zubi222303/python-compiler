class TargetCodeGenerator:
    def __init__(self):
        self.registers = ['r0', 'r1', 'r2', 'r3']
        self.register_map = {}
        self.code = []
    
    def generate(self, tac_code):
        self.code = []
        self.register_map = {}
        
        for line in tac_code.split('\n'):
            if not line.strip():
                continue
                
            parts = line.split()
            op = parts[0]
            
            if op == "STORE":
                self.code.append(f"mov {parts[2]}, {parts[1]}")
            elif op == "LOAD":
                self.code.append(f"mov {parts[2]}, {parts[1]}")
            elif op in ["ADD", "SUB", "MUL", "DIV"]:
                self.code.append(f"{op.lower()} {parts[3]}, {parts[1]}, {parts[2]}")
            elif op == "PRINT":
                self.code.append(f"call printf, {parts[1]}")
            elif op == "IF_FALSE":
                self.code.append(f"cmp {parts[1]}, 0")
                self.code.append(f"je {parts[3]}")
            elif op == "GOTO":
                self.code.append(f"jmp {parts[1]}")
            elif op == "LABEL":
                self.code.append(f"{parts[1]}:")
            elif op == "FUNC_BEGIN":
                self.code.append(f"{parts[1]}:")
                self.code.append("push bp")
                self.code.append("mov bp, sp")
            elif op == "FUNC_END":
                self.code.append("pop bp")
                self.code.append("ret")
            elif op == "RETURN":
                if len(parts) > 1:
                    self.code.append(f"mov ax, {parts[1]}")
                self.code.append("ret")
        
        return "\n".join(self.code)