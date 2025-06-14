from my_ast import ASTNode

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

    def add_symbol(self, name, symbol_type, scope_level, is_function=False, params=None, return_type=None):
        self.symbols[name] = {
            'type': symbol_type,
            'scope_level': scope_level,
            'is_function': is_function,
            'params': params or [],
            'return_type': return_type
        }

    def lookup(self, name, current_scope_only=False):
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol
        if not current_scope_only and self.parent:
            return self.parent.lookup(name)
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = SymbolTable()
        self.errors = []
        self.scope_level = 0
        self.current_function_return_type = None

    def analyze(self, ast):
        self.visit(ast)
        return self.errors

    def error(self, message, node):
        self.errors.append({
            'line': node.line if hasattr(node, 'line') else -1,
            'column': node.column if hasattr(node, 'column') else -1,
            'message': message
        })

    def visit(self, node):
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Block(self, node):
        self.scope_level += 1
        new_scope = SymbolTable(parent=self.current_scope)
        self.current_scope = new_scope
        
        for child in node.children:
            self.visit(child)
        
        self.current_scope = self.current_scope.parent
        self.scope_level -= 1

    def visit_Declaration(self, node):
        if len(node.children) < 2:
            self.error("Invalid declaration syntax", node)
            return
        
        var_type_node = node.children[0]
        var_name_node = node.children[1]
        
        var_name = var_name_node.value
        var_type = var_type_node.value
        
        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(f"Variable '{var_name}' already declared in this scope", var_name_node)
            return
        
        expr_type = None
        if len(node.children) > 2 and node.children[2].type != 'NoValue':
            expr_node = node.children[2]
            expr_type = self.visit(expr_node)
            if expr_type and not self.check_type_compatibility(var_type, expr_type):
                self.error(f"Type mismatch: cannot assign {expr_type} to {var_type}", expr_node)
        
        self.current_scope.add_symbol(var_name, var_type, self.scope_level)
        return var_type

    def visit_Assignment(self, node):
        if len(node.children) < 2:
            self.error("Invalid assignment syntax", node)
            return
        
        var_name_node = node.children[0]
        expr_node = node.children[1]
        
        var_name = var_name_node.value
        symbol = self.current_scope.lookup(var_name)
        if not symbol:
            self.error(f"Undeclared variable '{var_name}'", var_name_node)
            return
        
        expr_type = self.visit(expr_node)
        if expr_type and not self.check_type_compatibility(symbol['type'], expr_type):
            self.error(f"Type mismatch: cannot assign {expr_type} to {symbol['type']}", expr_node)
        
        return symbol['type']

    def visit_Function(self, node):
        if len(node.children) < 3:
            self.error("Invalid function definition", node)
            return
        
        name_node = node.children[0]
        params_node = node.children[1]
        body_node = node.children[2]
        return_type_node = node.children[3] if len(node.children) > 3 else None
        
        func_name = name_node.value
        return_type = return_type_node.value if return_type_node else None
        
        if self.current_scope.lookup(func_name, current_scope_only=True):
            self.error(f"Function '{func_name}' already declared in this scope", name_node)
            return
        
        previous_function_return_type = self.current_function_return_type
        self.current_function_return_type = return_type
        
        self.scope_level += 1
        new_scope = SymbolTable(parent=self.current_scope)
        self.current_scope = new_scope
        
        params = []
        for param in params_node.children:
            if len(param.children) < 2:
                continue
            param_type_node = param.children[0]
            param_name_node = param.children[1]
            param_type = param_type_node.value
            param_name = param_name_node.value
            params.append((param_type, param_name))
            self.current_scope.add_symbol(param_name, param_type, self.scope_level)
        
        self.current_scope.parent.add_symbol(
            func_name, 
            'function', 
            self.scope_level - 1,
            is_function=True,
            params=params,
            return_type=return_type
        )
        
        self.visit(body_node)
        
        self.current_scope = self.current_scope.parent
        self.scope_level -= 1
        self.current_function_return_type = previous_function_return_type
        
        return return_type or 'void'

    def visit_FunctionCall(self, node):
        func_name = node.value
        symbol = self.current_scope.lookup(func_name)
        if not symbol or not symbol['is_function']:
            self.error(f"Undeclared function '{func_name}'", node)
            return None
        
        if len(node.children) != len(symbol['params']):
            self.error(f"Function '{func_name}' expects {len(symbol['params'])} arguments but got {len(node.children)}", node)
            return symbol['return_type']
        
        for i, (arg_node, (param_type, _)) in enumerate(zip(node.children, symbol['params'])):
            arg_type = self.visit(arg_node)
            if arg_type and not self.check_type_compatibility(param_type, arg_type):
                self.error(f"Argument {i+1} type mismatch: expected {param_type}, got {arg_type}", arg_node)
        
        return symbol['return_type']

    def visit_IfStatement(self, node):
        if len(node.children) < 2:
            self.error("Invalid if statement", node)
            return
        
        condition_node = node.children[0]
        condition_type = self.visit(condition_node)
        if condition_type and condition_type != 'HaaNaa':
            self.error("If condition must be boolean", condition_node)
        
        for child in node.children[1:]:
            self.visit(child)

    def visit_WhileLoop(self, node):
        if len(node.children) < 2:
            self.error("Invalid while loop", node)
            return
        
        condition_node = node.children[0]
        condition_type = self.visit(condition_node)
        if condition_type and condition_type != 'HaaNaa':
            self.error("While condition must be boolean", condition_node)
        
        block_node = node.children[1]
        self.visit(block_node)

    def visit_Output(self, node):
        if not node.children:
            self.error("Invalid output statement", node)
            return
        
        expr_node = node.children[0]
        self.visit(expr_node)

    def visit_BinaryOp(self, node):
        if len(node.children) < 2:
            self.error("Invalid binary operation", node)
            return None
        
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        
        op = node.value
        if op in ['+', '-', '*', '/', '%']:
            if left_type not in ['Ginti', 'PointWala'] or right_type not in ['Ginti', 'PointWala']:
                self.error(f"Operator '{op}' requires numeric operands", node)
                return None
            if left_type == 'PointWala' or right_type == 'PointWala':
                return 'PointWala'
            return 'Ginti'
        elif op in ['<', '<=', '>', '>=']:
            if left_type not in ['Ginti', 'PointWala'] or right_type not in ['Ginti', 'PointWala']:
                self.error(f"Comparison operator '{op}' requires numeric operands", node)
                return None
            return 'HaaNaa'
        elif op in ['==', '!=']:
            if left_type != right_type:
                self.error(f"Cannot compare {left_type} with {right_type}", node)
                return None
            return 'HaaNaa'
        elif op in ['&&', '||']:
            if left_type != 'HaaNaa' or right_type != 'HaaNaa':
                self.error(f"Logical operator '{op}' requires boolean operands", node)
                return None
            return 'HaaNaa'
        
        return None

    def visit_Variable(self, node):
        var_name = node.value
        symbol = self.current_scope.lookup(var_name)
        if not symbol:
            self.error(f"Undeclared variable '{var_name}'", node)
            return None
        return symbol['type']

    def visit_Number(self, node):
        if '.' in node.value:
            return 'PointWala'
        return 'Ginti'

    def visit_String(self, node):
        return 'Baat'

    def visit_Boolean(self, node):
        return 'HaaNaa'

    def check_type_compatibility(self, target_type, source_type):
        if target_type == source_type:
            return True
        if target_type == 'PointWala' and source_type == 'Ginti':
            return True
        return False