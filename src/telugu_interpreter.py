from telugu_parser import TeluguParser, NumberNode, BinOpNode, AssignNode, VariableNode, PrintNode, IfNode, StringNode, BooleanNode, ForLoopNode
from telugu_lexer import TeluguLexer

class TeluguInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, ast):
        if isinstance(ast, NumberNode):
            return ast.value
        elif isinstance(ast, StringNode):
            return ast.value
        elif isinstance(ast, BooleanNode):
            return ast.value
        elif isinstance(ast, BinOpNode):
            left = self.interpret(ast.left)
            right = self.interpret(ast.right)
            if ast.op == '+':
                return left + right
            elif ast.op == '-':
                return left - right
            elif ast.op == '*':
                return left * right
            elif ast.op == '/':
                return left / right
            elif ast.op == '>':
                return left > right
            elif ast.op == '<':
                return left < right
            elif ast.op == '>=':
                return left >= right
            elif ast.op == '<=':
                return left <= right
            elif ast.op == '==':
                return left == right
            elif ast.op == '!=':
                return left != right
        elif isinstance(ast, AssignNode):
            value = self.interpret(ast.value)
            self.variables[ast.name] = value
            return value
        elif isinstance(ast, VariableNode):
            return self.variables.get(ast.name, 0)
        elif isinstance(ast, PrintNode):
            value = self.interpret(ast.value)
            print(value)
            return value
        elif isinstance(ast, IfNode):
            condition = self.interpret(ast.condition)
            if condition:
                return self.interpret(ast.true_body)
            elif ast.false_body:
                return self.interpret(ast.false_body)
        elif isinstance(ast, ForLoopNode):
            self.interpret(ast.init)
            while self.interpret(ast.condition):
                self.interpret(ast.body)
                self.interpret(ast.update)
        elif isinstance(ast, list):
            result = None
            for node in ast:
                result = self.interpret(node)
            return result
        else:
            raise ValueError(f"Unknown node type: {type(ast)}")

    def run(self, code):
        if not isinstance(code, str):
            raise ValueError("Input to run() must be a string")

        lexer = TeluguLexer()
        parser = TeluguParser()

        tokens = lexer.tokenize(code)
        print(f"Debug: Number of tokens: {len(tokens)}")
        print(f"Debug: First few tokens: {tokens[:5]}")

        ast = parser.parse(tokens)
        print(f"Debug: AST type: {type(ast)}")
        print(f"Debug: AST structure: {ast}")

        return self.interpret(ast)

if __name__ == "__main__":
    interpreter = TeluguInterpreter()

    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 telugu_interpreter.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    print(f"Debug: Type of code: {type(code)}")
    print(f"Debug: Content of code: {code[:100]}...")  # Print first 100 characters

    interpreter.run(code)
