import ply.lex as lex

# List of token names
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'GREATER',
    'LESS',
    'IF',
    'ELSE',
    'PRINT',
    'VARIABLE',
    'STRING',
    'LBRACE',
    'RBRACE',
)

class TeluguLexer:
    tokens = tokens  # Make tokens accessible as a class attribute

    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_EQUALS  = r'='
    t_GREATER = r'>'
    t_LESS    = r'<'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'

    # Regular expression rules with actions
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IF(self, t):
        r'యెడల'
        return t

    def t_ELSE(self, t):
        r'లేక'
        return t

    def t_PRINT(self, t):
        r'చేపాయిపిండి'
        return t

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]  # Remove the quotation marks
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

# Test it out
if __name__ == "__main__":
    data = '''
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)

    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    '''

    # Create an instance of TeluguLexer
    lexer = TeluguLexer()

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
