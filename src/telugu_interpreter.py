from telugu_parser import TeluguParser, NumberNode, BinOpNode, AssignNode, VariableNode, PrintNode, IfNode, StringNode, BooleanNode, ForLoopNode, MethodCallNode, ListNode
from telugu_lexer import TeluguLexer

class TeluguInterpreter:
    def __init__(self):
        self.variables = {}
        self.గణితం = MathModule()

    def interpret(self, ast):
        if isinstance(ast, str):
            lexer = TeluguLexer()
            parser = TeluguParser()
            tokens = lexer.tokenize(ast)
            ast = parser.parse(tokens)

        if isinstance(ast, NumberNode):
            return ast.value
        elif isinstance(ast, StringNode):
            return ast.value
        elif isinstance(ast, BooleanNode):
            return ast.value
        elif isinstance(ast, BinOpNode):
            left = self.interpret(ast.left)
            right = self.interpret(ast.right)
            print(f"Debug: BinOpNode - Left: {left}, Right: {right}, Op: {ast.op}")
            result = None  # Initialize result variable
            if ast.op == '+':
                result = left + right  # Perform addition without string conversion
            elif ast.op == '-':
                result = left - right
            elif ast.op == '*':
                result = left * right
            elif ast.op == '/':
                result = left / right
            elif ast.op == '>':
                result = left > right
            elif ast.op == '<':
                result = left < right
            elif ast.op == '>=':
                result = left >= right
            elif ast.op == '<=':
                result = left <= right
            elif ast.op == '==':
                result = left == right
            elif ast.op == '!=':
                result = left != right
            else:
                raise ValueError(f"Unknown operator: {ast.op}")
            print(f"Debug: BinOpNode result: {result}")
            return result
        elif isinstance(ast, AssignNode):
            value = self.interpret(ast.value)
            self.variables[ast.name] = value
            print(f"Debug: AssignNode - Name: {ast.name}, Value: {value}")
            return value
        elif isinstance(ast, VariableNode):
            value = self.variables.get(ast.name, 0)
            print(f"Debug: VariableNode - Name: {ast.name}, Value: {value}")
            return value
        elif isinstance(ast, PrintNode):
            value = self.interpret(ast.value)
            print(value)
            return value
        elif isinstance(ast, IfNode):
            condition = bool(self.interpret(ast.condition))
            print(f"Debug: IfNode condition evaluated to: {condition}")
            if condition:
                print("Debug: Executing true branch")
                return self.interpret(ast.true_body)
            elif ast.false_body:
                print("Debug: Executing false branch")
                return self.interpret(ast.false_body)
            else:
                print("Debug: No false branch, skipping")
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
        elif isinstance(ast, ListNode):
            return [self.interpret(element) for element in ast.elements]
        elif isinstance(ast, MethodCallNode):
            print(f"Debug: MethodCallNode - Object: {ast.object}, Method: {ast.method}")
            if isinstance(ast.object, VariableNode) and ast.object.name == 'గణితం':
                print(f"Debug: Accessing MathModule method: {ast.method}")
                method = getattr(self.గణితం, ast.method)
                args = [self.interpret(arg) for arg in ast.args]
                return method(*args)
            elif isinstance(ast.object, VariableNode) and ast.object.name == 'ఫైల్':
                print(f"Debug: Accessing File operation method: {ast.method}")
                args = [self.interpret(arg) for arg in ast.args]
                if ast.method == 'వ్రాయి':
                    return self.file_write(*args)
                elif ast.method == 'చదువు':
                    return self.file_read(*args)
            else:
                print(f"Debug: Accessing object method: {ast.method}")
                obj = self.interpret(ast.object)
                args = [self.interpret(arg) for arg in ast.args]
                if isinstance(obj, str) and ast.method == 'చేర్చు':
                    return obj + ''.join(args)
                elif isinstance(obj, list) and ast.method == 'చేర్చు':
                    obj.append(args[0])
                    return obj
                method = getattr(obj, ast.method)
                return method(*args)
        else:
            raise ValueError(f"Unknown node type: {type(ast)}")

    def file_write(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return True

    def file_read(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def చేర్చు(self, string, *args):
        return string + ''.join(args)

class MathModule:
    def పవర్(self, base, exponent):
        return base ** exponent

    def __init__(self):
        self.variables = {}
        # Removed recursive instantiation of MathModule

    def interpret(self, ast):
        if isinstance(ast, str):
            lexer = TeluguLexer()
            parser = TeluguParser()
            tokens = lexer.tokenize(ast)
            ast = parser.parse(tokens)

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
        elif isinstance(ast, MethodCallNode):
            obj = self.interpret(ast.object)
            args = [self.interpret(arg) for arg in ast.args]
            method = getattr(obj, ast.method)
            return method(*args)
        else:
            raise ValueError(f"Unknown node type: {type(ast)}")

class MathModule:
    def పవర్(self, base, exponent):
        return base ** exponent

    def __init__(self):
        self.variables = {}
        # Removed recursive instantiation of MathModule

# The duplicate MathModule class has been removed.
# The run method has been moved to the TeluguInterpreter class.

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

    interpreter.interpret(code)

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

    interpreter.interpret(code)
