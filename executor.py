class Executor:
    def __init__(self):
        self.memory = {}
        self.output = []
        self.pc = 0  # Program counter
        self.registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0}
    
    def execute_tac(self, tac_code):
        """Execute Three Address Code directly"""
        self.reset_state()
        instructions = [line.strip() for line in tac_code.split('\n') if line.strip()]
        
        while self.pc < len(instructions):
            instruction = instructions[self.pc]
            self.pc += 1
            
            try:
                parts = instruction.split()
                op = parts[0]
                
                if op == "STORE":
                    src = self.get_value(parts[1])
                    dest = parts[2]
                    self.memory[dest] = src
                    
                elif op == "LOAD":
                    value = parts[1].strip("'") if parts[1].startswith("'") else int(parts[1])
                    dest = parts[2]
                    self.memory[dest] = value
                    
                elif op == "ADD":
                    src1 = self.get_value(parts[1])
                    src2 = self.get_value(parts[2])
                    dest = parts[3]
                    self.memory[dest] = src1 + src2
                    
                elif op == "SUB":
                    src1 = self.get_value(parts[1])
                    src2 = self.get_value(parts[2])
                    dest = parts[3]
                    self.memory[dest] = src1 - src2
                    
                elif op == "PRINT":
                    value = self.get_value(parts[1])
                    self.output.append(str(value))
                    
                elif op == "IF_FALSE":
                    condition = self.get_value(parts[1])
                    if not condition:
                        self.pc = self.find_label(instructions, parts[3])
                        
                elif op == "GOTO":
                    self.pc = self.find_label(instructions, parts[1])
                    
                elif op == "LABEL":
                    continue  # Handled during jumps
                    
                # Add other operations as needed...
                
            except Exception as e:
                raise RuntimeError(f"Error executing '{instruction}': {str(e)}")
        
        return '\n'.join(self.output)
    
    def get_value(self, identifier):
        """Get value from memory or registers"""
        if identifier in self.registers:
            return self.registers[identifier]
        return self.memory.get(identifier, identifier)
    
    def find_label(self, instructions, label):
        """Find instruction index for a label"""
        for i, instr in enumerate(instructions):
            if instr.startswith(f"LABEL {label}"):
                return i
        raise ValueError(f"Label {label} not found")
    
    def reset_state(self):
        """Reset execution state"""
        self.memory = {}
        self.output = []
        self.pc = 0
        self.registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0}