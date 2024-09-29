class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class TeluguLexer:
    def __init__(self):
        self.keywords = {
            'చర': 'VAR',
            'యెడల': 'IF',
            'లేక': 'ELSE',
            'చేపాయిపిండి': 'PRINT',
            'నిజం': 'TRUE',
            'అబద్ధం': 'FALSE',
            'మరియు': 'AND',
            'లేదా': 'OR',
            'కాదు': 'NOT',
            'వరకు': 'WHILE',
            'కొరకు': 'FOR',
            'తిరిగిఇవ్వు': 'RETURN',
            'చేయు': 'DO'
        }

        self.operators = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '=': 'ASSIGN',
            '==': 'EQUALS',
            '>': 'GREATER',
            '<': 'LESS',
            '>=': 'GREATER_EQUAL',
            '<=': 'LESS_EQUAL',
            '!=': 'NOT_EQUAL',
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACE',
            '}': 'RBRACE',
            '.': 'DOT',
            ',': 'COMMA',
            ';': 'SEMICOLON'
        }

        self.telugu_chars = set('అఆఇఈఉఊఋఌఎఏఐఒఓఔంఃాిీుూృౄెేైొోౌ్')

    def tokenize(self, code):
        tokens = []
        i = 0
        print(f"Debug: Starting tokenization of code: {code}")
        while i < len(code):
            print(f"Debug: Current character: '{code[i]}' at position {i}")
            # Skip whitespace
            if isinstance(code[i], str) and code[i].isspace():
                print(f"Debug: Skipping whitespace at position {i}")
                i += 1
                continue

            if isinstance(code[i], str) and code[i] == '#':
                print(f"Debug: Found comment at position {i}")
                while i < len(code) and code[i] != '\n':
                    i += 1
                continue

            if isinstance(code[i], str) and (code[i] in self.telugu_chars or code[i].isalpha()):
                word = ''
                print(f"Debug: Starting word at position {i}")
                while i < len(code) and isinstance(code[i], str) and (code[i] in self.telugu_chars or code[i].isalnum() or code[i] == '_'):
                    word += code[i]
                    i += 1
                print(f"Debug: Completed word: '{word}'")
                if word in self.keywords:
                    tokens.append(Token(self.keywords[word], word))
                    print(f"Debug: Added keyword token: {tokens[-1]}")
                else:
                    tokens.append(Token('IDENTIFIER', word))
                    print(f"Debug: Added identifier token: {tokens[-1]}")
                continue

            if isinstance(code[i], str) and code[i].isdigit():
                number = ''
                print(f"Debug: Starting number at position {i}")
                while i < len(code) and isinstance(code[i], str) and (code[i].isdigit() or code[i] == '.'):
                    number += code[i]
                    i += 1
                print(f"Debug: Completed number: '{number}'")
                if '.' in number:
                    tokens.append(Token('FLOAT', float(number)))
                else:
                    tokens.append(Token('INTEGER', int(number)))
                print(f"Debug: Added number token: {tokens[-1]}")
                continue

            if isinstance(code[i], str) and (code[i] == '"' or code[i] == "'"):
                string = ''
                quote = code[i]
                i += 1
                print(f"Debug: Starting string at position {i}")
                while i < len(code) and isinstance(code[i], str) and code[i] != quote:
                    string += code[i]
                    i += 1
                if i < len(code) and isinstance(code[i], str) and code[i] == quote:
                    tokens.append(Token('STRING', string))
                    i += 1
                    print(f"Debug: Added string token: {tokens[-1]}")
                else:
                    raise ValueError("Unterminated string")
                continue

            if isinstance(code[i], str) and code[i:i+2] in self.operators:
                tokens.append(Token(self.operators[code[i:i+2]], code[i:i+2]))
                print(f"Debug: Added two-character operator token: {tokens[-1]}")
                i += 2
            elif isinstance(code[i], str) and code[i] in self.operators:
                tokens.append(Token(self.operators[code[i]], code[i]))
                print(f"Debug: Added single-character operator token: {tokens[-1]}")
                i += 1
            elif isinstance(code[i], str) and code[i] in '(){}[]':
                tokens.append(Token(code[i], code[i]))
                print(f"Debug: Added parenthesis/bracket token: {tokens[-1]}")
                i += 1
            else:
                print(f"Debug: Unknown character '{code[i]}' at position {i}")
                raise ValueError(f"Unknown character: {code[i]}")

        print(f"Debug: Tokenization complete. Total tokens: {len(tokens)}")
        return tokens

if __name__ == "__main__":
    lexer = TeluguLexer()
    code = """
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)

    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    """
    tokens = lexer.tokenize(code)
    for token in tokens:
        print(token)
