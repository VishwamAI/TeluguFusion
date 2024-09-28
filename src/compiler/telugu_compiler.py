from telugu_parser import TeluguParser, NumberNode, BinOpNode, AssignNode, VariableNode, PrintNode, IfNode, StringNode
from telugu_lexer import TeluguLexer

class TeluguCompiler:
    def __init__(self):
        self.parser = TeluguParser()
        self.bytecode = []
        self.variables = {}
        self.label_counter = 0

    def compile(self, code):
        lexer = TeluguLexer()
        tokens = lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.generate_bytecode(ast)
        return self.bytecode

    def generate_bytecode(self, statements):
        for statement in statements:
            self.compile_node(statement)

    def compile_node(self, node):
        if isinstance(node, NumberNode):
            self.bytecode.append(('PUSH', node.value))
        elif isinstance(node, StringNode):
            self.bytecode.append(('PUSH', node.value))
        elif isinstance(node, BinOpNode):
            self.compile_node(node.left)
            self.compile_node(node.right)
            if node.op == '+':
                self.bytecode.append(('ADD',))
            elif node.op == '-':
                self.bytecode.append(('SUB',))
            elif node.op == '*':
                self.bytecode.append(('MUL',))
            elif node.op == '/':
                self.bytecode.append(('DIV',))
            elif node.op == '>':
                self.bytecode.append(('GT',))
            elif node.op == '<':
                self.bytecode.append(('LT',))
        elif isinstance(node, AssignNode):
            self.compile_node(node.value)
            self.variables[node.name] = len(self.variables)
            self.bytecode.append(('STORE', self.variables[node.name]))
        elif isinstance(node, VariableNode):
            if node.name in self.variables:
                self.bytecode.append(('LOAD', self.variables[node.name]))
            else:
                raise NameError(f"Variable '{node.name}' is not defined")
        elif isinstance(node, PrintNode):
            self.compile_node(node.value)
            self.bytecode.append(('PRINT',))
        elif isinstance(node, IfNode):
            self.compile_node(node.condition)
            label_else = self.new_label()
            label_end = self.new_label()
            self.bytecode.append(('JUMP_IF_FALSE', label_else))
            self.generate_bytecode(node.true_body)
            self.bytecode.append(('JUMP', label_end))
            self.bytecode.append(('LABEL', label_else))
            if node.false_body:
                self.generate_bytecode(node.false_body)
            self.bytecode.append(('LABEL', label_end))
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

if __name__ == "__main__":
    compiler = TeluguCompiler()
    test_code = '''
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)

    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    '''
    bytecode = compiler.compile(test_code)
    print("Compilation completed.")
    print("Bytecode:", bytecode)
