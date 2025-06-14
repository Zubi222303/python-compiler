from my_ast import ASTNode

class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_scope = "global"
    
    def generate(self, ast):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.visit(ast)
        return self.code
    
    def visit(self, node):
        if not isinstance(node, ASTNode):
            return
        
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        results = []
        for child in node.children:
            results.append(self.visit(child))
        return results
    
    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_Declaration(self, node):
        var_type = node.children[0].value
        var_name = node.children[1].value
        
        if len(node.children) > 2 and node.children[2].type != 'NoValue':
            expr_result = self.visit(node.children[2])
            self.code.append(f"STORE {expr_result} {var_name}")
    
    def visit_Assignment(self, node):
        var_name = node.children[0].value
        expr_result = self.visit(node.children[1])
        self.code.append(f"STORE {expr_result} {var_name}")
    
    def visit_BinaryOp(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        temp = self.new_temp()
        
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '%': 'MOD',
            '&&': 'AND',
            '||': 'OR',
            '==': 'EQ',
            '!=': 'NEQ',
            '<': 'LT',
            '<=': 'LTE',
            '>': 'GT',
            '>=': 'GTE'
        }
        
        op = op_map.get(node.value, node.value)
        self.code.append(f"{op} {left} {right} {temp}")
        return temp
    
    def visit_Number(self, node):
        temp = self.new_temp()
        self.code.append(f"LOAD {node.value} {temp}")
        return temp
    
    def visit_Variable(self, node):
        return node.value
    
    def visit_String(self, node):
        temp = self.new_temp()
        self.code.append(f"LOAD '{node.value}' {temp}")
        return temp
    
    def visit_Boolean(self, node):
        temp = self.new_temp()
        value = 1 if node.value == 'Sahi' else 0
        self.code.append(f"LOAD {value} {temp}")
        return temp
    
    def visit_Output(self, node):
        expr_result = self.visit(node.children[0])
        self.code.append(f"PRINT {expr_result}")
    
    def visit_IfStatement(self, node):
        condition = self.visit(node.children[0])
        true_label = self.new_label()
        false_label = self.new_label()
        end_label = self.new_label()
        
        self.code.append(f"IF_FALSE {condition} GOTO {false_label}")
        self.code.append(f"GOTO {true_label}")
        self.code.append(f"LABEL {true_label}")
        
        # Process true block
        self.visit(node.children[1])
        self.code.append(f"GOTO {end_label}")
        
        # Process else/elif blocks if any
        self.code.append(f"LABEL {false_label}")
        i = 2
        while i < len(node.children):
            if i + 1 < len(node.children) and node.children[i+1].type == 'BinaryOp':  # elif condition
                elif_condition = self.visit(node.children[i+1])
                elif_true_label = self.new_label()
                next_elif_label = self.new_label()
                
                self.code.append(f"IF_FALSE {elif_condition} GOTO {next_elif_label}")
                self.code.append(f"GOTO {elif_true_label}")
                self.code.append(f"LABEL {elif_true_label}")
                
                self.visit(node.children[i+2])  # elif block
                self.code.append(f"GOTO {end_label}")
                self.code.append(f"LABEL {next_elif_label}")
                
                i += 3
            else:  # else block
                self.visit(node.children[i])
                i += 1
        
        self.code.append(f"LABEL {end_label}")
    
    def visit_WhileLoop(self, node):
        start_label = self.new_label()
        condition_label = self.new_label()
        end_label = self.new_label()
        
        self.code.append(f"LABEL {start_label}")
        self.code.append(f"GOTO {condition_label}")
        self.code.append(f"LABEL {condition_label}")
        
        condition = self.visit(node.children[0])
        self.code.append(f"IF_FALSE {condition} GOTO {end_label}")
        
        self.visit(node.children[1])  # while block
        self.code.append(f"GOTO {start_label}")
        self.code.append(f"LABEL {end_label}")
    
    def visit_Function(self, node):
        func_name = node.children[0].value
        params = node.children[1].children
        body = node.children[2]
        return_type = node.children[3].value if len(node.children) > 3 and node.children[3].value else 'void'
        
        # Save current scope
        old_scope = self.current_scope
        self.current_scope = func_name
        
        # Function prologue
        self.code.append(f"FUNC_BEGIN {func_name} {return_type}")
        
        # Parameters
        for param in params:
            param_name = param.children[1].value
            param_type = param.children[0].value
            self.code.append(f"PARAM {param_name} {param_type}")
        
        # Function body
        self.visit(body)
        
        # Function epilogue
        self.code.append(f"FUNC_END {func_name}")
        
        # Restore scope
        self.current_scope = old_scope
    
    def visit_Return(self, node):
        if node.children[0].type != 'NoReturnValue':
            expr_result = self.visit(node.children[0])
            self.code.append(f"RETURN {expr_result}")
        else:
            self.code.append("RETURN")
    
    def visit_FunctionCall(self, node):
        func_name = node.value
        args = [self.visit(arg) for arg in node.children]
        temp = self.new_temp()
        
        for arg in args:
            self.code.append(f"ARG {arg}")
        
        self.code.append(f"CALL {func_name} {temp}")
        return temp