from telugu_lexer import TeluguLexer
from telugu_parser import TeluguParser

class TeluguInterpreter:
    def __init__(self):
        self.parser = TeluguParser()
        self.variables = {}

    def interpret(self, code):
        ast = self.parser.parse(code)
        return self.evaluate(ast)

    def evaluate(self, node):
        if isinstance(node, tuple):
            if node[0] == 'program':
                return self.evaluate(node[1])
            elif node[0] == 'assignment':
                var_name, value = node[1], self.evaluate(node[2])
                self.variables[var_name] = value
                return value
            elif node[0] == 'if':
                condition, body = node[1], node[2]
                if self.evaluate(condition):
                    return self.evaluate(body)
            elif node[0] == 'if_else':
                condition, if_body, else_body = node[1], node[2], node[3]
                if self.evaluate(condition):
                    return self.evaluate(if_body)
                else:
                    return self.evaluate(else_body)
            elif node[0] == 'while':
                condition, body = node[1], node[2]
                while self.evaluate(condition):
                    self.evaluate(body)
            elif node[0] == 'print':
                value = self.evaluate(node[1])
                print(value)
                return value
            elif node[0] in ['+', '-', '*', '/', '%', '<', '>', '<=', '>=', '==']:
                left, right = self.evaluate(node[1]), self.evaluate(node[2])
                if node[0] == '+': return left + right
                elif node[0] == '-': return left - right
                elif node[0] == '*': return left * right
                elif node[0] == '/': return left / right
                elif node[0] == '%': return left % right
                elif node[0] == '<': return left < right
                elif node[0] == '>': return left > right
                elif node[0] == '<=': return left <= right
                elif node[0] == '>=': return left >= right
                elif node[0] == '==': return left == right
        elif isinstance(node, list):
            result = None
            for statement in node:
                result = self.evaluate(statement)
            return result
        elif isinstance(node, str):
            if node.isdigit():
                return int(node)
            elif node in self.variables:
                return self.variables[node]
            else:
                raise NameError(f"Variable '{node}' is not defined")
        else:
            return node

# Test the interpreter
if __name__ == "__main__":
    interpreter = TeluguInterpreter()

    test_code = """
    x = 5;
    y = 3;
    z = x + y;
    ప్రింట్(z);
    ఒకవేళ (z > 7) {
        ప్రింట్("z is greater than 7");
    } లేకపోతే {
        ప్రింట్("z is not greater than 7");
    }
    """

    print("Running Telugu code:")
    print(test_code)
    print("\nOutput:")
    interpreter.interpret(test_code)
