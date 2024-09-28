from telugu_parser import TeluguParser, NumberNode, BinOpNode, AssignNode, VariableNode, PrintNode, IfNode, StringNode, MethodCallNode, ForLoopNode, ListNode
from telugu_lexer import TeluguLexer
class TeluguInterpreter:
    def __init__(self):
        self.parser = TeluguParser()
        self.variables = {}
        self.math_function_map = {
            'పవర్': 'pow',
            'వర్గమూలం': 'sqrt',
            'సైన్': 'sin',
            'కొసైన్': 'cos',
            'టాంజెంట్': 'tan',
            'లాగ్': 'log'
        }

    def interpret(self, code):
        lexer = TeluguLexer()
        tokens = lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        return self.execute_statements(ast)

    def execute_statements(self, statements):
        result = None
        for statement in statements:
            result = self.execute(statement)
        return result

    def execute(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, BinOpNode):
            left = self.execute(node.left)
            right = self.execute(node.right)
            if node.op == 'PLUS':
                # Ensure variables are evaluated before concatenation
                left_value = self.variables.get(left, left) if isinstance(left, str) else left
                right_value = self.variables.get(right, right) if isinstance(right, str) else right
                if isinstance(left_value, str) or isinstance(right_value, str):
                    return str(left_value) + str(right_value)
                return left_value + right_value
            elif node.op == 'MINUS':
                return left - right
            elif node.op == 'MULTIPLY':
                return left * right
            elif node.op == 'DIVIDE':
                return left / right
            elif node.op == 'GREATER':
                return left > right
            elif node.op == 'LESS':
                return left < right
            elif node.op == 'LESS_EQUAL':
                return left <= right
        elif isinstance(node, AssignNode):
            value = self.execute(node.value)
            self.variables[node.name] = value
            return value
        elif isinstance(node, VariableNode):
            return self.variables.get(node.name, 0)
        elif isinstance(node, PrintNode):
            value = self.execute(node.value)
            print(value)
            return value
        elif isinstance(node, IfNode):
            condition = self.execute(node.condition)
            if condition:
                return self.execute_statements(node.true_body)
            elif node.false_body:
                return self.execute_statements(node.false_body)
        elif isinstance(node, MethodCallNode):
            obj = self.execute(node.object)
            if obj == 'ఫైల్':
                # Handle file operations
                return self.execute_file_operation(node)
            elif isinstance(obj, (int, float)):
                # Handle built-in math functions
                return self.execute_math_function(node, obj)
            elif isinstance(obj, str):
                # Handle string methods
                return self.execute_string_method(node, obj)
            elif isinstance(obj, list):
                # Handle list methods
                return self.execute_list_method(node, obj)
            else:
                raise ValueError(f"Unsupported object type for method call: {type(obj)}")
        elif isinstance(node, ForLoopNode):
            print(f"Debug: Executing ForLoopNode")
            self.execute(node.init)
            print(f"Debug: After init, i = {self.variables.get('i', 0)}")
            result = None
            while True:
                condition = self.execute(node.condition)
                print(f"Debug: Loop condition evaluated to: {condition}")
                if not condition:
                    break
                print(f"Debug: Loop condition true, executing body")
                result = self.execute_statements(node.body)
                print(f"Debug: After body execution, మొత్తం = {self.variables.get('మొత్తం', 0)}")
                self.execute(node.update)
                print(f"Debug: After update, i = {self.variables.get('i', 0)}")
            print(f"Debug: Loop finished, final మొత్తం = {self.variables.get('మొత్తం', 0)}")
            return result
        elif isinstance(node, ListNode):
            return [self.execute(element) for element in node.elements]
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def execute_file_operation(self, node):
        file_operation_map = {
            'వ్రాయి': 'write',
            'చదువు': 'read'
        }
        method_name = file_operation_map.get(node.method)
        if method_name:
            args = [self.execute(arg) for arg in node.args]
            if method_name == 'write':
                with open(args[0], 'w') as f:
                    f.write(args[1])
                return None
            elif method_name == 'read':
                with open(args[0], 'r') as f:
                    return f.read()
        else:
            raise ValueError(f"Unsupported file operation: {node.method}")

    def execute_math_function(self, node, obj):
        import math
        if node.method in ['వ్రాయి', 'చదువు']:
            return self.execute_file_operation(node)
        method_name = self.math_function_map.get(node.method, node.method)
        method = getattr(math, method_name)
        args = [self.execute(arg) for arg in node.args]
        return method(*args)

    def execute_string_method(self, node, obj):
        if node.method == 'చేర్చు':
            # Special handling for చేర్చు (concatenation) method
            args = [self.execute(arg) for arg in node.args]
            return obj + ''.join(args)  # Concatenate obj with all arguments
        else:
            string_method_map = {
                'విభజించు': 'split',
                'మార్చు': 'replace',
                'తొలగించు': 'strip'
            }
            method_name = string_method_map.get(node.method, node.method)
            method = getattr(obj, method_name)
            args = [self.execute(arg) for arg in node.args]
            return method(*args)
    def execute_list_method(self, node, obj):
        if node.method == 'చేర్చు':
            args = [self.execute(arg) for arg in node.args]
            obj.extend(args)
            return obj
        else:
            raise ValueError(f"Unsupported list method: {node.method}")

if __name__ == "__main__":
    interpreter = TeluguInterpreter()
    test_code = '''
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)

    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    '''
    result = interpreter.interpret(test_code)
    print("Interpretation completed.")
