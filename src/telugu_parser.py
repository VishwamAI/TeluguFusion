from telugu_lexer import TeluguLexer, Token

# Define the AST node classes
class Node:
    pass

class BooleanNode(Node):
    def __init__(self, value):
        self.value = value

class ListNode(Node):
    def __init__(self, elements):
        self.elements = elements

class ForLoopNode(Node):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class MethodCallNode(Node):
    def __init__(self, object, method, args):
        self.object = object
        self.method = method
        self.args = args

class PropertyAccessNode(Node):
    def __init__(self, object, property):
        self.object = object
        self.property = property

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class AssignNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VariableNode(Node):
    def __init__(self, name):
        self.name = name

class PrintNode(Node):
    def __init__(self, value):
        self.value = value

class IfNode(Node):
    def __init__(self, condition, true_body, false_body=None):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

class StringNode(Node):
    def __init__(self, value):
        self.value = value

class TeluguParser:
    def __init__(self):
        self.lexer = TeluguLexer()
        self.tokens = []
        self.current_token = None
        self.token_index = -1
        self.parser = self  # Initialize the parser attribute

    def parse(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        ast = self.parse_statements()
        print(f"Debug: AST structure: {ast}")  # Debug print
        return ast

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            print(f"Debug: Advanced to token: {self.current_token}")  # Debug statement
        else:
            self.current_token = None
            print("Debug: Advanced to end of tokens")  # Debug statement

    def expect(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            print(f"Debug: Expected and found token: {token}")  # Debug statement
            self.advance()
            return token
        raise SyntaxError(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")

    def parse_statements(self):
        statements = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type == 'VAR':
                statements.append(self.parse_assignment())
            elif self.current_token.type == 'PRINT':
                statements.append(self.parse_print())
            elif self.current_token.type == 'IF':
                statements.append(self.parse_if())
            elif self.current_token.value == 'కోసం':
                statements.append(self.parse_for_loop())
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token}")
        return statements

    def parse_for_loop(self):
        print("Parsing for loop")
        self.expect('IDENTIFIER')  # 'కోసం'
        print(f"Current token after IDENTIFIER: {self.current_token}")
        self.expect('LPAREN')
        print(f"Current token after LPAREN: {self.current_token}")

        # Parse initialization
        if self.current_token.type == 'VAR':
            init = self.parse_assignment()
        elif self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.advance()
            if self.current_token.type == 'ASSIGN':
                self.advance()
                value = self.parse_expression()
                init = AssignNode(var_name, value)
            else:
                self.token_index -= 1  # Step back to re-parse the identifier
                self.current_token = self.tokens[self.token_index]
                init = self.parse_expression()
        else:
            raise SyntaxError(f"Expected VAR or IDENTIFIER, got {self.current_token.type}")
        print(f"Parsed init: {init}")
        self.expect('SEMICOLON')
        print(f"Current token after first SEMICOLON: {self.current_token}")

        # Parse condition
        condition = self.parse_expression()
        print(f"Parsed condition: {condition}")
        self.expect('SEMICOLON')
        print(f"Current token after second SEMICOLON: {self.current_token}")

        # Parse update
        update = self.parse_assignment() if self.current_token.type == 'IDENTIFIER' else self.parse_expression()
        print(f"Parsed update: {update}")

        # Ensure RPAREN is present and handle any unexpected tokens
        while self.current_token.type != 'RPAREN':
            if self.current_token.type in ['SEMICOLON', 'ASSIGN', 'IDENTIFIER']:
                self.advance()  # Skip unexpected semicolons, assignments, or identifiers
            else:
                raise SyntaxError(f"Unexpected token in for loop: {self.current_token}")
        self.expect('RPAREN')
        print(f"Current token after RPAREN: {self.current_token}")

        self.expect('LBRACE')
        body = self.parse_statements()
        self.expect('RBRACE')
        print("Finished parsing for loop")
        return ForLoopNode(init, condition, update, body)

    def peek_next_token(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None

    def parse_statements(self):
        statements = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type == 'VAR':
                statements.append(self.parse_assignment())
            elif self.current_token.type == 'PRINT':
                statements.append(self.parse_print())
            elif self.current_token.type == 'IF':
                statements.append(self.parse_if())
            elif self.current_token.value == 'కోసం':
                statements.append(self.parse_for_loop())
            elif self.current_token.value == 'ఫైల్':
                statements.append(self.parse_file_operation())
            elif self.current_token.type == 'IDENTIFIER':
                if self.peek_next_token() and self.peek_next_token().type == 'ASSIGN':
                    statements.append(self.parse_assignment())
                elif self.peek_next_token() and self.peek_next_token().type == 'DOT':
                    statements.append(self.parse_method_call())
                else:
                    statements.append(self.parse_expression())
            elif self.current_token.type == 'SEMICOLON':
                self.advance()  # Skip semicolons
            else:
                self.advance()  # Skip unexpected tokens
        return statements

    def parse_file_operation(self):
        self.expect('IDENTIFIER')  # 'ఫైల్'
        self.expect('DOT')
        method = self.expect('IDENTIFIER').value
        self.expect('LPAREN')
        args = self.parse_arguments()
        self.expect('RPAREN')
        return MethodCallNode(VariableNode('ఫైల్'), method, args)

    def parse_file_operation(self):
        self.expect('IDENTIFIER')  # 'ఫైల్'
        self.expect('DOT')
        method = self.expect('IDENTIFIER').value
        self.expect('LPAREN')
        args = self.parse_arguments()
        self.expect('RPAREN')
        return MethodCallNode(VariableNode('ఫైల్'), method, args)

    def parse_file_operation(self):
        method = self.expect('IDENTIFIER').value
        self.expect('DOT')
        operation = self.expect('IDENTIFIER').value
        self.expect('LPAREN')
        args = self.parse_arguments()
        self.expect('RPAREN')
        return MethodCallNode(VariableNode(method), operation, args)

    def parse_file_operation(self):
        method = self.expect('IDENTIFIER').value
        self.expect('DOT')
        operation = self.expect('IDENTIFIER').value
        self.expect('LPAREN')
        args = self.parse_arguments()
        self.expect('RPAREN')
        return MethodCallNode(VariableNode(method), operation, args)

    def parse_arguments(self):
        args = []
        while self.current_token and self.current_token.type != 'RPAREN':
            args.append(self.parse_expression())
            if self.current_token.type == 'COMMA':
                self.advance()
        return args

    def parse_assignment(self):
        if self.current_token.type == 'VAR':
            self.advance()
        var_name = self.expect('IDENTIFIER').value
        self.expect('ASSIGN')
        value = self.parse_expression()
        return AssignNode(var_name, value)

    def parse_print(self):
        self.expect('PRINT')
        self.expect('LPAREN')
        value = self.parse_expression()
        self.expect('RPAREN')
        return PrintNode(value)

    def parse_if(self):
        self.expect('IF')
        self.expect('LPAREN')
        condition = self.parse_expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        true_body = self.parse_statements()
        self.expect('RBRACE')
        false_body = None
        if self.current_token and self.current_token.type == 'ELSE':
            self.advance()
            self.expect('LBRACE')
            false_body = self.parse_statements()
            self.expect('RBRACE')
        return IfNode(condition, true_body, false_body)

    def parse_expression(self):
        if self.current_token.type in ['TRUE', 'FALSE']:
            value = self.current_token.type == 'TRUE'
            self.advance()
            return BooleanNode(value)
        expr = self.parse_comparison()
        while self.current_token and self.current_token.type == 'DOT':
            self.advance()
            if self.current_token.type != 'IDENTIFIER':
                raise SyntaxError("Expected method or property name after '.'")
            method = self.current_token.value
            self.advance()
            if self.current_token and self.current_token.type == 'LPAREN':
                self.advance()
                args = []
                if self.current_token.type != 'RPAREN':
                    args = self.parse_arguments()
                self.expect('RPAREN')
                expr = MethodCallNode(expr, method, args)
            else:
                expr = PropertyAccessNode(expr, method)
        return expr

    def parse_comparison(self):
        expr = self.parse_arithmetic()
        while self.current_token and self.current_token.type in ['GREATER', 'LESS', 'EQUALS', 'GREATER_EQUAL', 'LESS_EQUAL', 'NOT_EQUAL']:
            op_token = self.current_token.type
            op_str = {
                'GREATER': '>', 'LESS': '<', 'EQUALS': '==',
                'GREATER_EQUAL': '>=', 'LESS_EQUAL': '<=', 'NOT_EQUAL': '!='
            }.get(op_token, op_token)
            self.advance()
            right = self.parse_arithmetic()
            expr = BinOpNode(expr, op_str, right)
        return expr

    def parse_arithmetic(self):
        expr = self.parse_term()
        while self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
            op_token = self.current_token.type
            op_str = {
                'PLUS': '+',
                'MINUS': '-'
            }.get(op_token, op_token)
            self.advance()
            right = self.parse_term()
            expr = BinOpNode(expr, op_str, right)
        return expr

    def parse_term(self):
        expr = self.parse_factor()
        while self.current_token and self.current_token.type in ['MULTIPLY', 'DIVIDE']:
            op_token = self.current_token.type
            op_str = {
                'MULTIPLY': '*',
                'DIVIDE': '/'
            }.get(op_token, op_token)
            self.advance()
            right = self.parse_factor()
            expr = BinOpNode(expr, op_str, right)
        return expr

    def parse_factor(self):
        if self.current_token.type == 'INTEGER':
            value = int(self.current_token.value)
            self.advance()
            return NumberNode(value)
        elif self.current_token.type == 'FLOAT':
            value = float(self.current_token.value)
            self.advance()
            return NumberNode(value)
        elif self.current_token.type == 'IDENTIFIER':
            value = self.current_token.value
            self.advance()
            return VariableNode(value)
        elif self.current_token.type == 'STRING':
            value = self.current_token.value
            self.advance()
            return StringNode(value)
        elif self.current_token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        elif self.current_token.type == '[':
            return self.parse_list()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_list(self):
        elements = []
        self.expect('[')
        while self.current_token.type != ']':
            elements.append(self.parse_expression())
            if self.current_token.type == 'COMMA':
                self.advance()
            elif self.current_token.type != ']':
                raise SyntaxError(f"Expected ',' or ']', got {self.current_token.type}")
        self.expect(']')
        return ListNode(elements)
    def parse_method_call(self):
        object = self.parse_factor()
        self.expect('DOT')
        method = self.expect('IDENTIFIER')
        self.expect('LPAREN')
        arguments = self.parse_arguments()
        self.expect('RPAREN')
        return MethodCallNode(object, method.value, arguments)

# Test the parser
if __name__ == "__main__":
    parser = TeluguParser()

    test_input = '''
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)

    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    '''

    result = parser.parse(test_input)
    print("Parsing completed.")
    print("AST:", result)
