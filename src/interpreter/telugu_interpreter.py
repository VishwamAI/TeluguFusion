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
        # Initialize variables with default values
        self.variables = {'సంఖ్య': 0, 'పేరు': '', 'జతపడి': False, 'మొత్తం': 0}

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
        print(f"Debug: Executing node of type {type(node)}")
        if isinstance(node, NumberNode):
            print(f"Debug: NumberNode - Value: {node.value}")
            return node.value
        elif isinstance(node, StringNode):
            print(f"Debug: StringNode - Value: {node.value}")
            return node.value
        elif isinstance(node, BinOpNode):
            print(f"Debug: BinOpNode - Starting execution")
            print(f"Debug: Left node: {node.left}")
            print(f"Debug: Right node: {node.right}")
            left = self.execute(node.left)
            right = self.execute(node.right)
            print(f"Debug: BinOpNode - Left: {left} (type: {type(left)}), Right: {right} (type: {type(right)}), Op: {node.op}")
            if node.op == '+':
                # Ensure variables are evaluated before concatenation
                print(f"Debug: Before evaluation - Left: {left} (type: {type(left)}), Right: {right} (type: {type(right)})")
                left_value = self._evaluate_value(left)
                right_value = self._evaluate_value(right)
                print(f"Debug: After evaluation - Left: {left_value} (type: {type(left_value)}), Right: {right_value} (type: {type(right_value)})")
                # Convert both operands to strings before concatenation
                left_str = str(left_value) if left_value is not None else ''
                right_str = str(right_value) if right_value is not None else ''
                print(f"Debug: Before concatenation - Left: {left_str} (type: {type(left_str)}), Right: {right_str} (type: {type(right_str)})")
                print(f"Debug: Attempting concatenation of '{left_str}' and '{right_str}'")
                result = left_str + right_str
                print(f"Debug: Concatenation result: {result} (type: {type(result)})")
                return result
            elif node.op == '-':
                return self._ensure_numeric(left) - self._ensure_numeric(right)
            elif node.op == '*':
                return self._ensure_numeric(left) * self._ensure_numeric(right)
            elif node.op == '/':
                return self._ensure_numeric(left) / self._ensure_numeric(right)
            elif node.op == '>':
                return self._ensure_comparable(left) > self._ensure_comparable(right)
            elif node.op == '<':
                return self._ensure_comparable(left) < self._ensure_comparable(right)
            elif node.op == '<=':
                return self._ensure_comparable(left) <= self._ensure_comparable(right)
        elif isinstance(node, AssignNode):
            value = self.execute(node.value)
            self.variables[node.name] = value
            print(f"Debug: AssignNode - Name: {node.name}, Value: {value} (type: {type(value)})")
            print(f"Debug: Variables after assignment: {self.variables}")
            return value
        elif isinstance(node, VariableNode):
            value = self.variables.get(node.name, 0)  # Default to 0 for numeric operations
            if isinstance(value, str) and not value:
                value = ''  # Use empty string for string operations
            print(f"Debug: VariableNode - Name: {node.name}, Value: {value} (type: {type(value)})")
            print(f"Debug: Current variables: {self.variables}")
            return value
        elif isinstance(node, PrintNode):
            value = self.execute(node.value)
            print(f"Debug: PrintNode - Value: {value} (type: {type(value)})")
            print(value)
            return value
        elif isinstance(node, IfNode):
            condition = self.execute(node.condition)
            print(f"Debug: IfNode - Condition: {condition} (type: {type(condition)})")
            if condition:
                return self.execute_statements(node.true_body)
            elif node.false_body:
                return self.execute_statements(node.false_body)
        elif isinstance(node, MethodCallNode):
            obj = self.execute(node.object)
            print(f"Debug: MethodCallNode - Object: {obj} (type: {type(obj)}), Method: {node.method}")
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
            elements = [self.execute(element) for element in node.elements]
            print(f"Debug: ListNode - Elements: {elements}")
            return elements
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def _ensure_numeric(self, value):
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Cannot convert '{value}' to a number")
        else:
            raise ValueError(f"Unsupported type for numeric operation: {type(value)}")

    def _ensure_comparable(self, value):
        if isinstance(value, (int, float, str)):
            return value
        else:
            raise ValueError(f"Unsupported type for comparison: {type(value)}")

    def _evaluate_value(self, value):
        if isinstance(value, str) and value in self.variables:
            return self.variables[value]
        return value

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
# Trigger GitHub Actions workflow
# Adding a comment to trigger the workflow
