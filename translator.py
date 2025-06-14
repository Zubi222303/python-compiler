class PythonTranslator:
    @staticmethod
    def tac_to_python(tac_code):
        """Convert TAC to executable Python code"""
        python_code = [
            "def execute():",
            "    memory = {}",
            "    output = []"
        ]
        
        for line in tac_code.split('\n'):
            if not line.strip():
                continue
                
            parts = line.split()
            op = parts[0]
            
            if op == "STORE":
                python_code.append(f"    memory['{parts[2]}'] = memory.get('{parts[1]}', {parts[1]})")
                
            elif op == "LOAD":
                value = parts[1]
                if value.replace('.','',1).isdigit():
                    python_code.append(f"    memory['{parts[2]}'] = {value}")
                else:
                    python_code.append(f"    memory['{parts[2]}'] = '{value.strip("'")}'")
                    
            elif op == "ADD":
                python_code.append(
                    f"    memory['{parts[3]}'] = "
                    f"memory.get('{parts[1]}', {parts[1]}) + "
                    f"memory.get('{parts[2]}', {parts[2]})"
                )
                
            elif op == "PRINT":
                python_code.append(f"    output.append(str(memory.get('{parts[1]}', '{parts[1]}')))")
                
            elif op == "IF_FALSE":
                python_code.append(f"    if not memory.get('{parts[1]}', {parts[1]}):")
                python_code.append(f"        pass  # GOTO {parts[3]} implementation needed")
                
            # Add other operations as needed...
        
        python_code.append("    return '\\n'.join(output)")
        python_code.append("result = execute()")
        return '\n'.join(python_code)