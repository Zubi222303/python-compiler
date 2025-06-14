from lexer import Token
from my_ast import ASTNode

class ParseTreeNode:
    def __init__(self, rule_name, children=None, token=None):
        self.rule = rule_name
        self.children = children or []
        self.token = token
    
    def __repr__(self, level=0):
        ret = "  " * level + f"{self.rule}"
        if self.token:
            ret += f" [Token: {self.token.value}]"
        ret += "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.parse_tree = ParseTreeNode("Program")
        self.ast = ASTNode('Program')
        self.sync_tokens = [';', '}', 'Bas']

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(None, 'EOF', -1, -1)

    def peek(self, n=1):
        return self.tokens[self.pos + n] if self.pos + n < len(self.tokens) else Token(None, 'EOF', -1, -1)

    def advance(self):
        self.pos += 1
        return self.tokens[self.pos - 1] if self.pos - 1 < len(self.tokens) else Token(None, 'EOF', -1, -1)

    def expect(self, expected_types, message=None):
        token = self.current()
        if token.type in expected_types or token.value in expected_types:
            return self.advance()
        
        expected_str = ', '.join(f"'{t}'" for t in expected_types)
        error_msg = f"Expected {expected_str}, found '{token.value}'"
        if message:
            error_msg += f" ({message})"
            
        self.errors.append({
            'line': token.line,
            'column': token.column,
            'message': error_msg
        })
        return None

    def synchronize(self):
        while self.current().value not in self.sync_tokens and self.current().type != 'EOF':
            self.advance()
        return self.current()

    def parse(self):
        while self.pos < len(self.tokens):
            try:
                stmt_parse, stmt_ast = self.statement()
                if stmt_parse and stmt_ast:
                    self.parse_tree.children.append(stmt_parse)
                    self.ast.children.append(stmt_ast)
                else:
                    token = self.current()
                    self.errors.append({
                        'line': token.line,
                        'column': token.column,
                        'message': f"Unexpected token '{token.value}'"
                    })
                    self.advance()
            except Exception as e:
                token = self.current()
                self.errors.append({
                    'line': token.line,
                    'column': token.column,
                    'message': f"Parsing error: {str(e)}"
                })
                self.synchronize()
        return self.parse_tree, self.ast

    def statement(self):
        token = self.current()
        if token.type == 'KEYWORD':
            if token.value == 'Rakho':
                return self.declaration()
            elif token.value == 'Dikhao':
                return self.output_statement()
            elif token.value == 'Agar':
                return self.if_statement()
            elif token.value == 'JabTak':
                return self.while_loop()
            elif token.value == 'Kaam':
                return self.function_definition()
            elif token.value == 'Wapis':
                return self.return_statement()
        elif token.type == 'IDENTIFIER':
            next_token = self.peek()
            if next_token and next_token.type == 'ASSIGN':
                return self.assignment_statement()
            elif next_token and next_token.value == '(':
                return self.function_call()
        elif token.value == '{':
            return self.block()
        return None, None

    def block(self):
        start = self.expect(['{'], "Expected '{' to start block")
        block_parse = ParseTreeNode("Block")
        block_ast = ASTNode('Block', line=start.line, column=start.column)
        
        while self.current().value != '}' and self.current().type != 'EOF':
            stmt_parse, stmt_ast = self.statement()
            if stmt_parse and stmt_ast:
                block_parse.children.append(stmt_parse)
                block_ast.children.append(stmt_ast)
            else:
                break
        
        self.expect(['}'], "Expected '}' to end block")
        return block_parse, block_ast

    def declaration(self):
        start = self.expect(['Rakho'], "Expected 'Rakho'")
        decl_parse = ParseTreeNode("Declaration")
        
        dtype = self.expect(['Ginti', 'PointWala', 'Baat', 'HaaNaa'], "Expected data type")
        decl_parse.children.append(ParseTreeNode("Type", token=dtype))
        
        var = self.expect(['IDENTIFIER'], "Expected variable name")
        decl_parse.children.append(ParseTreeNode("Variable", token=var))
        
        if self.current().type == 'ASSIGN':
            self.expect(['ASSIGN'], "Expected '='")
            expr_parse, expr_ast = self.expression()
            decl_parse.children.append(expr_parse)
        else:
            expr_ast = ASTNode('NoValue')
        
        self.expect([';'], "Expected ';'")
        
        decl_ast = ASTNode('Declaration', [
            ASTNode('Type', value=dtype.value, line=dtype.line, column=dtype.column),
            ASTNode('Variable', value=var.value, line=var.line, column=var.column),
            expr_ast
        ], line=start.line, column=start.column)
        
        return decl_parse, decl_ast

    def return_statement(self):
        start = self.expect(['Wapis'], "Expected 'Wapis'")
        return_parse = ParseTreeNode("ReturnStatement")
        
        if self.current().value != ';':
            expr_parse, expr_ast = self.expression()
            return_parse.children.append(expr_parse)
        else:
            expr_ast = ASTNode('NoReturnValue')
        
        self.expect([';'], "Expected ';' after return statement")
        
        return_ast = ASTNode('Return', [expr_ast], line=start.line, column=start.column)
        return return_parse, return_ast

    def output_statement(self):
        token = self.expect(['Dikhao'], "Expected 'Dikhao'")
        out_parse = ParseTreeNode("OutputStatement", token=token)
        
        expr_parse, expr_ast = self.expression()
        out_parse.children.append(expr_parse)
        
        self.expect([';'], "Expected ';'")
        
        out_ast = ASTNode('Output', [expr_ast], line=token.line, column=token.column)
        return out_parse, out_ast

    def assignment_statement(self):
        var = self.expect(['IDENTIFIER'], "Expected variable name")
        assign_parse = ParseTreeNode("Assignment", token=var)
        
        self.expect(['ASSIGN'], "Expected '='")
        expr_parse, expr_ast = self.expression()
        assign_parse.children.append(expr_parse)
        
        self.expect([';'], "Expected ';'")
        
        assign_ast = ASTNode('Assignment', [
            ASTNode('Variable', value=var.value, line=var.line, column=var.column),
            expr_ast
        ], line=var.line, column=var.column)
        
        return assign_parse, assign_ast

    def if_statement(self):
        start = self.expect(['Agar'], "Expected 'Agar'")
        if_parse = ParseTreeNode("IfStatement")
        
        self.expect(['('], "Expected '(' after 'Agar'")
        cond_parse, cond_ast = self.expression()
        if_parse.children.append(cond_parse)
        self.expect([')'], "Expected ')' after condition")
        
        block_parse, block_ast = self.block()
        if_parse.children.append(block_parse)
        
        if_nodes = [cond_ast, block_ast]
        
        while self.current().value in ['WarnaAgar', 'Warna']:
            if self.current().value == 'WarnaAgar':
                elif_token = self.advance()
                elif_parse = ParseTreeNode("ElseIf", token=elif_token)
                
                self.expect(['('], "Expected '(' after 'WarnaAgar'")
                elif_cond_parse, elif_cond_ast = self.expression()
                elif_parse.children.append(elif_cond_parse)
                self.expect([')'], "Expected ')' after condition")
                
                elif_block_parse, elif_block_ast = self.block()
                elif_parse.children.append(elif_block_parse)
                
                if_parse.children.append(elif_parse)
                if_nodes.extend([elif_cond_ast, elif_block_ast])
            else:
                else_token = self.advance()
                else_parse = ParseTreeNode("Else", token=else_token)
                
                else_block_parse, else_block_ast = self.block()
                else_parse.children.append(else_block_parse)
                
                if_parse.children.append(else_parse)
                if_nodes.append(else_block_ast)
        
        if_ast = ASTNode('IfStatement', if_nodes, line=start.line, column=start.column)
        return if_parse, if_ast

    def while_loop(self):
        start = self.expect(['JabTak'], "Expected 'JabTak'")
        while_parse = ParseTreeNode("WhileLoop")
        
        self.expect(['('], "Expected '(' after 'JabTak'")
        cond_parse, cond_ast = self.expression()
        while_parse.children.append(cond_parse)
        self.expect([')'], "Expected ')' after condition")
        
        block_parse, block_ast = self.block()
        while_parse.children.append(block_parse)
        
        while_ast = ASTNode('WhileLoop', [cond_ast, block_ast], line=start.line, column=start.column)
        return while_parse, while_ast

    def function_definition(self):
        start = self.expect(['Kaam'], "Expected 'Kaam'")
        func_parse = ParseTreeNode("FunctionDefinition")
        
        name = self.expect(['IDENTIFIER'], "Expected function name")
        func_parse.children.append(ParseTreeNode("FunctionName", token=name))
        
        self.expect(['('], "Expected '(' after function name")
        
        params_parse = ParseTreeNode("Parameters")
        params_ast = []
        while self.current().value != ')' and self.current().type != 'EOF':
            param_type = self.expect(['Ginti', 'PointWala', 'Baat', 'HaaNaa'], "Expected parameter type")
            param_name = self.expect(['IDENTIFIER'], "Expected parameter name")
            
            param_parse = ParseTreeNode("Parameter")
            param_parse.children.append(ParseTreeNode("Type", token=param_type))
            param_parse.children.append(ParseTreeNode("Variable", token=param_name))
            params_parse.children.append(param_parse)
            
            params_ast.append(ASTNode('Parameter', [
                ASTNode('Type', value=param_type.value),
                ASTNode('Variable', value=param_name.value)
            ]))
            
            if self.current().value == ',':
                self.advance()
            else:
                break
        
        func_parse.children.append(params_parse)
        self.expect([')'], "Expected ')' after parameters")

        # Handle optional return type declaration
        return_type = None
        if self.current().value == 'Wapis':
            return_token = self.advance()
            return_type = self.expect(['Ginti', 'PointWala', 'Baat', 'HaaNaa'], "Expected return type")
            func_parse.children.append(ParseTreeNode("ReturnType", token=return_type))
        
        body_parse, body_ast = self.block()
        func_parse.children.append(body_parse)
        
        func_ast = ASTNode('Function', [
            ASTNode('Name', value=name.value),
            ASTNode('Parameters', params_ast),
            body_ast,
            ASTNode('ReturnType', value=return_type.value if return_type else None)
        ], line=start.line, column=start.column)
        
        return func_parse, func_ast

    def function_call(self):
        fn = self.expect(['IDENTIFIER'])
        call_parse = ParseTreeNode("FunctionCall", token=fn)
        
        self.expect(['('], "Expected '(' in function call")
        
        args_parse = ParseTreeNode("Arguments")
        args_ast = []
        while self.current().value != ')' and self.current().type != 'EOF':
            arg_parse, arg_ast = self.expression()
            args_parse.children.append(arg_parse)
            args_ast.append(arg_ast)
            
            if self.current().value == ',':
                self.advance()
            else:
                break
        
        call_parse.children.append(args_parse)
        self.expect([')'], "Expected ')' after function arguments")
        self.expect([';'], "Expected ';' after function call")
        
        call_ast = ASTNode('FunctionCall', args_ast, value=fn.value, line=fn.line, column=fn.column)
        return call_parse, call_ast

    def expression(self):
        left_parse, left_ast = self.logical_or()
        return left_parse, left_ast

    def logical_or(self):
        left_parse, left_ast = self.logical_and()
        parse_node = left_parse
        
        while self.current().value == '||':
            op = self.advance()
            right_parse, right_ast = self.logical_and()
            
            new_parse = ParseTreeNode("BinaryOp")
            new_parse.children = [parse_node, ParseTreeNode("Operator", token=op), right_parse]
            parse_node = new_parse
            
            left_ast = ASTNode('BinaryOp', [left_ast, right_ast], value=op.value, line=op.line, column=op.column)
        
        return parse_node, left_ast

    def logical_and(self):
        left_parse, left_ast = self.equality()
        parse_node = left_parse
        
        while self.current().value == '&&':
            op = self.advance()
            right_parse, right_ast = self.equality()
            
            new_parse = ParseTreeNode("BinaryOp")
            new_parse.children = [parse_node, ParseTreeNode("Operator", token=op), right_parse]
            parse_node = new_parse
            
            left_ast = ASTNode('BinaryOp', [left_ast, right_ast], value=op.value, line=op.line, column=op.column)
        
        return parse_node, left_ast

    def equality(self):
        left_parse, left_ast = self.relational()
        parse_node = left_parse
        
        while self.current().value in ['==', '!=']:
            op = self.advance()
            right_parse, right_ast = self.relational()
            
            new_parse = ParseTreeNode("BinaryOp")
            new_parse.children = [parse_node, ParseTreeNode("Operator", token=op), right_parse]
            parse_node = new_parse
            
            left_ast = ASTNode('BinaryOp', [left_ast, right_ast], value=op.value, line=op.line, column=op.column)
        
        return parse_node, left_ast

    def relational(self):
        left_parse, left_ast = self.additive()
        parse_node = left_parse
        
        while self.current().value in ['<', '<=', '>', '>=']:
            op = self.advance()
            right_parse, right_ast = self.additive()
            
            new_parse = ParseTreeNode("BinaryOp")
            new_parse.children = [parse_node, ParseTreeNode("Operator", token=op), right_parse]
            parse_node = new_parse
            
            left_ast = ASTNode('BinaryOp', [left_ast, right_ast], value=op.value, line=op.line, column=op.column)
        
        return parse_node, left_ast

    def additive(self):
        left_parse, left_ast = self.multiplicative()
        parse_node = left_parse
        
        while self.current().value in ['+', '-']:
            op = self.advance()
            right_parse, right_ast = self.multiplicative()
            
            new_parse = ParseTreeNode("BinaryOp")
            new_parse.children = [parse_node, ParseTreeNode("Operator", token=op), right_parse]
            parse_node = new_parse
            
            left_ast = ASTNode('BinaryOp', [left_ast, right_ast], value=op.value, line=op.line, column=op.column)
        
        return parse_node, left_ast

    def multiplicative(self):
        left_parse, left_ast = self.primary()
        parse_node = left_parse
        
        while self.current().value in ['*', '/', '%']:
            op = self.advance()
            right_parse, right_ast = self.primary()
            
            new_parse = ParseTreeNode("BinaryOp")
            new_parse.children = [parse_node, ParseTreeNode("Operator", token=op), right_parse]
            parse_node = new_parse
            
            left_ast = ASTNode('BinaryOp', [left_ast, right_ast], value=op.value, line=op.line, column=op.column)
        
        return parse_node, left_ast

    def primary(self):
        token = self.current()
        if token.type in ['NUMBER_INT', 'NUMBER_FLOAT']:
            self.advance()
            parse_node = ParseTreeNode("Number", token=token)
            ast_node = ASTNode('Number', value=token.value, line=token.line, column=token.column)
            return parse_node, ast_node
        elif token.type == 'STRING':
            self.advance()
            parse_node = ParseTreeNode("String", token=token)
            ast_node = ASTNode('String', value=token.value, line=token.line, column=token.column)
            return parse_node, ast_node
        elif token.value == '(':
            self.advance()
            parse_node = ParseTreeNode("Parenthesized")
            expr_parse, expr_ast = self.expression()
            parse_node.children.append(expr_parse)
            self.expect([')'], "Expected ')' after expression")
            return parse_node, expr_ast
        elif token.type == 'IDENTIFIER':
            if self.peek().value == '(':
                return self.function_call()
            else:
                self.advance()
                parse_node = ParseTreeNode("Variable", token=token)
                ast_node = ASTNode('Variable', value=token.value, line=token.line, column=token.column)
                return parse_node, ast_node
        elif token.value in ['Sahi', 'Ghalat']:
            self.advance()
            parse_node = ParseTreeNode("Boolean", token=token)
            ast_node = ASTNode('Boolean', value=token.value, line=token.line, column=token.column)
            return parse_node, ast_node
        else:
            self.errors.append({
                'line': token.line,
                'column': token.column,
                'message': f"Unexpected expression token '{token.value}'"
            })
            self.advance()
            parse_node = ParseTreeNode("Unknown", token=token)
            ast_node = ASTNode('Unknown')
            return parse_node, ast_node