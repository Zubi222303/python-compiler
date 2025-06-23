from my_ast import ASTNode

class OutputGenerator:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.output_lines = []
        self.return_value = None
        self.break_loop = False

    def evaluate(self, node):
        method_name = f"eval_{node.type}"
        method = getattr(self, method_name, self.generic_eval)
        return method(node)

    def generic_eval(self, node):
        for child in node.children:
            self.evaluate(child)

    def eval_Program(self, node):
        for child in node.children:
            self.evaluate(child)

    def eval_Declaration(self, node):
        if len(node.children) >= 2:
            var_name = node.children[1].value
            value = self.evaluate(node.children[2]) if len(node.children) > 2 else None
            self.variables[var_name] = value

    def eval_Assignment(self, node):
        var_name = node.children[0].value
        value = self.evaluate(node.children[1])
        self.variables[var_name] = value

    def eval_Number(self, node):
        return float(node.value) if '.' in node.value else int(node.value)

    def eval_String(self, node):
        return str(node.value)

    def eval_Boolean(self, node):
        return True if node.value == 'Sahi' else False

    def eval_Variable(self, node):
        return self.variables.get(node.value, 0)

    def eval_BinaryOp(self, node):
        left = self.evaluate(node.children[0])
        right = self.evaluate(node.children[1])
        op = node.value

        try:
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right
            elif op == '%': return left % right
            elif op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '<=': return left <= right
            elif op == '>': return left > right
            elif op == '>=': return left >= right
            elif op == '&&': return left and right
            elif op == '||': return left or right
        except Exception as e:
            self.output_lines.append(f"Error in operation {op}: {str(e)}")
            return None

    def eval_Output(self, node):
        value = self.evaluate(node.children[0])
        self.output_lines.append(str(value))

    def eval_Function(self, node):
        name = node.children[0].value
        self.functions[name] = node  # Store full AST node

    def eval_FunctionCall(self, node):
        func_name = node.value
        func_node = self.functions.get(func_name)
        if not func_node:
            self.output_lines.append(f"Error: Function '{func_name}' not found")
            return None

        param_defs = func_node.children[1].children
        func_body = func_node.children[2]

        args = [self.evaluate(arg) for arg in node.children]

        # Save previous scope
        old_vars = self.variables.copy()

        # Bind parameters
        for i, param in enumerate(param_defs):
            param_name = param.children[1].value
            self.variables[param_name] = args[i]

        # Execute function body
        self.return_value = None
        self.evaluate(func_body)

        # Restore scope
        self.variables = old_vars
        return self.return_value

    def eval_Return(self, node):
        if node.children:
            self.return_value = self.evaluate(node.children[0])

    def eval_IfStatement(self, node):
        condition = self.evaluate(node.children[0])
        if condition:
            self.evaluate(node.children[1])  # if block
        elif len(node.children) > 2:
            self.evaluate(node.children[2])  # else block

    def eval_WhileLoop(self, node):
        condition_node = node.children[0]
        body_node = node.children[1]
        while self.evaluate(condition_node):
            self.evaluate(body_node)
            if self.break_loop:
                self.break_loop = False
                break

    def eval_Block(self, node):
        for child in node.children:
            self.evaluate(child)

    def eval_Break(self, node):
        self.break_loop = True


def generate_output_from_ast(ast):
    generator = OutputGenerator()
    generator.evaluate(ast)
    return "\n".join(generator.output_lines)
