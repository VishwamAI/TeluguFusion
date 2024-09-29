import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.compiler import TeluguCompiler
import time

def test_jit_performance():
    compiler = TeluguCompiler()

    test_code = '''
    చర సంఖ్య = 1
    చర మొత్తం = 0
    చేయు (సంఖ్య <= 1000000) {
        మొత్తం = మొత్తం + సంఖ్య
        సంఖ్య = సంఖ్య + 1
    }
    చేపాయిపిండి(మొత్తం)
    '''

    print("Testing JIT compilation performance...")

    # Measure compilation time
    start_time = time.time()
    compiler.compile(test_code)
    compile_time = time.time() - start_time
    print(f"Compilation time: {compile_time:.4f} seconds")

    # Measure execution time
    start_time = time.time()
    result = compiler.compile(test_code)
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time:.4f} seconds")

    print(f"Result: {result}")

    return compile_time, execution_time

if __name__ == "__main__":
    compile_time, execution_time = test_jit_performance()
    print(f"\nTotal time: {compile_time + execution_time:.4f} seconds")
