from compiler.telugu_compiler import TeluguCompiler
import os

def test_compiler():
    compiler = TeluguCompiler()

    # Read the sample .tel file
    with open('sample_program.tel', 'r', encoding='utf-8') as file:
        code = file.read()

    try:
        # Compile the code
        bytecode = compiler.compile(code)
        print("Compilation successful. Bytecode:")
        print(bytecode)

        # Verify the bytecode
        assert bytecode, "Bytecode generation failed."
        print("\nBytecode verification:")
        for instruction in bytecode:
            print(instruction)

    except Exception as e:
        print(f"Compilation failed: {str(e)}")
        assert False, f"Compilation failed: {str(e)}"

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = test_compiler()
    print(f"\nCompiler test {'passed' if success else 'failed'}.")
