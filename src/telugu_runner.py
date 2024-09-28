#!/usr/bin/env python3

import sys
import os
from telugu_interpreter import TeluguInterpreter
from compiler.telugu_compiler import TeluguCompiler
from telugu_parser import TeluguParser
from telugu_lexer import TeluguLexer

def run_tel_file(file_path, mode='interpret'):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    lexer = TeluguLexer()
    parser = TeluguParser()

    if mode == 'interpret':
        interpreter = TeluguInterpreter()
        ast = parser.parse(lexer.tokenize(code))
        result = interpreter.interpret(ast)
        print("Interpretation completed.")
        return result
    elif mode == 'compile':
        compiler = TeluguCompiler()
        ast = parser.parse(lexer.tokenize(code))
        compiled_code = compiler.compile(ast)
        output_file = os.path.splitext(file_path)[0] + '.py'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(compiled_code)
        print(f"Compilation completed. Output file: {output_file}")
        return output_file
    else:
        raise ValueError("Invalid mode. Use 'interpret' or 'compile'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: tel <file_path> [interpret|compile]")
        sys.exit(1)

    file_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'interpret'

    try:
        result = run_tel_file(file_path, mode)
        if mode == 'interpret':
            print("Execution result:", result)
        elif mode == 'compile':
            print(f"Compiled file created: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
