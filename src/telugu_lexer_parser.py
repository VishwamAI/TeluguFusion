import re
from llvmlite import ir
from llvmlite import binding as llvm

# Token types
TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_STRING = 'STRING'
TOKEN_ID = 'ID'
TOKEN_KEYWORD = 'KEYWORD'
TOKEN_OPERATOR = 'OPERATOR'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class TeluguLexer:
    def __init__(self):
        self.tokens = []
        self.keywords = ['చర', 'యెడల', 'లేక', 'చేపాయిపిండి']
        self.operators = ['+', '-', '*', '/', '>', '<', '=']

    def tokenize(self, code):
        token_specification = [
            ('FLOAT',   r'\d+\.\d+'),
            ('INT',     r'\d+'),
            ('ID',      r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('STRING',  r'"[^"]*"'),
            ('OP',      r'[+\-*/=><]'),
            ('NEWLINE', r'\n'),
            ('SKIP',    r'[ \t]+'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'ID' and value in self.keywords:
                kind = 'KEYWORD'
            elif kind == 'OP':
                kind = 'OPERATOR'
            elif kind == 'NEWLINE' or kind == 'SKIP':
                continue
            self.tokens.append(Token(kind, value))
        return self.tokens

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class AssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

class PrintNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IfNode(ASTNode):
    def __init__(self, condition, true_body, false_body=None):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class TeluguParser:
    def __init__(self):
        self.current_token = None
        self.token_index = -1

    def parse(self, tokens):
        self.tokens = tokens
        self.advance()
        return self.parse_statements()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse_statements(self):
        statements = []
        while self.current_token is not None:
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'చర':
                statements.append(self.parse_assignment())
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'చేపాయిపిండి':
                statements.append(self.parse_print())
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'యెడల':
                statements.append(self.parse_if())
            else:
                statements.append(self.parse_expression())
        return statements

    def parse_assignment(self):
        self.advance()  # Skip 'చర'
        name = self.current_token.value
        self.advance()
        self.advance()  # Skip '='
        value = self.parse_expression()
        return AssignNode(name, value)

    def parse_print(self):
        self.advance()  # Skip 'చేపాయిపిండి'
        value = self.parse_expression()
        return PrintNode(value)

    def parse_if(self):
        self.advance()  # Skip 'యెడల'
        condition = self.parse_expression()
        true_body = self.parse_statements()
        false_body = None
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'లేక':
            self.advance()  # Skip 'లేక'
            false_body = self.parse_statements()
        return IfNode(condition, true_body, false_body)

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-']:
            op = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = BinOpNode(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
            op = self.current_token.value
            self.advance()
            right = self.parse_factor()
            left = BinOpNode(left, op, right)
        return left

    def parse_factor(self):
        if self.current_token.type == 'INT':
            node = NumberNode(int(self.current_token.value))
            self.advance()
            return node
        elif self.current_token.type == 'FLOAT':
            node = NumberNode(float(self.current_token.value))
            self.advance()
            return node
        elif self.current_token.type == 'STRING':
            node = StringNode(self.current_token.value[1:-1])  # Remove quotes
            self.advance()
            return node
        elif self.current_token.type == 'ID':
            node = VariableNode(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
            self.advance()
            node = self.parse_expression()
            self.advance()  # Skip ')'
            return node

# Integration with LLVM
def generate_llvm_ir(ast):
    module = ir.Module(name="telugu_module")
    builder = ir.IRBuilder()

    # Define the main function
    main_type = ir.FunctionType(ir.IntType(32), [])
    main_func = ir.Function(module, main_type, name="main")
    block = main_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Generate LLVM IR for each statement in the AST
    for node in ast:
        if isinstance(node, AssignNode):
            value = generate_expression(builder, node.value)
            var = builder.alloca(ir.FloatType(), name=node.name)
            builder.store(value, var)
        elif isinstance(node, PrintNode):
            value = generate_expression(builder, node.value)
            printf = module.declare_printf()
            format_str = "%f\n\0"
            c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(format_str)),
                                bytearray(format_str.encode("utf8")))
            global_fmt = ir.GlobalVariable(module, c_fmt.type, name="fstr")
            global_fmt.linkage = 'internal'
            global_fmt.global_constant = True
            global_fmt.initializer = c_fmt
            fmt_arg = builder.bitcast(global_fmt, ir.IntType(8).as_pointer())
            builder.call(printf, [fmt_arg, value])
        elif isinstance(node, IfNode):
            cond_val = generate_expression(builder, node.condition)
            with builder.if_else(cond_val) as (then, otherwise):
                with then:
                    for stmt in node.true_body:
                        generate_llvm_ir([stmt])
                with otherwise:
                    if node.false_body:
                        for stmt in node.false_body:
                            generate_llvm_ir([stmt])

    # Add a return statement to the main function
    builder.ret(ir.Constant(ir.IntType(32), 0))

    return str(module)

def generate_expression(builder, node):
    if isinstance(node, NumberNode):
        return ir.Constant(ir.FloatType(), float(node.value))
    elif isinstance(node, BinOpNode):
        left = generate_expression(builder, node.left)
        right = generate_expression(builder, node.right)
        if node.op == '+':
            return builder.fadd(left, right)
        elif node.op == '-':
            return builder.fsub(left, right)
        elif node.op == '*':
            return builder.fmul(left, right)
        elif node.op == '/':
            return builder.fdiv(left, right)
        elif node.op == '>':
            return builder.fcmp_ordered('>', left, right)
        elif node.op == '<':
            return builder.fcmp_ordered('<', left, right)
    elif isinstance(node, VariableNode):
        return builder.load(builder.function.args[0])
    elif isinstance(node, StringNode):
        return ir.Constant(ir.ArrayType(ir.IntType(8), len(node.value) + 1),
                           bytearray(node.value.encode("utf8") + b"\00"))

# Main function to test the lexer and parser
if __name__ == "__main__":
    code = '''
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)
    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    '''

    lexer = TeluguLexer()
    tokens = lexer.tokenize(code)

    parser = TeluguParser()
    ast = parser.parse(tokens)

    print("Tokens:", tokens)
    print("AST:", ast)

    llvm_ir = generate_llvm_ir(ast)
    print("LLVM IR:", llvm_ir)
