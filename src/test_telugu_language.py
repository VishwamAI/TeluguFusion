import pytest
from integrated_framework import IntegratedFramework

@pytest.fixture
def framework():
    return IntegratedFramework()

def test_language_syntax(framework):
    # Test variable declaration and assignment
    code = "చర సంఖ్య = 10"
    result = framework.run(code, mode='interpret')
    assert result == 10

    # Test arithmetic operations
    code = "చర x = 5 + 3 * 2"
    result = framework.run(code, mode='interpret')
    assert result == 11

    # Test comparison operators
    code = "చర y = 10 > 5"
    result = framework.run(code, mode='interpret')
    assert result == True

def test_interpreter_functionality(framework):
    # Test if-else statement
    code = """
    చర సంఖ్య = 10
    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("పెద్దది")
    } లేక {
        చేపాయిపిండి("చిన్నది")
    }
    """
    result = framework.run(code, mode='interpret')
    assert result == "పెద్దది"

    # Test loop
    code = """
    చర మొత్తం = 0
    కోసం (చర i = 1; i <= 5; i = i + 1) {
        మొత్తం = మొత్తం + i;
    }
    చేపాయిపిండి(మొత్తం)
    """
    result = framework.run(code, mode='interpret')
    assert result == 15

def test_compiler_functionality(framework):
    code = "చర x = 5 + 3"
    bytecode = framework.run(code, mode='compile')
    assert isinstance(bytecode, list)
    assert any('PUSH' in instr for instr in bytecode)
    assert any('ADD' in instr for instr in bytecode)
    assert any('STORE' in instr for instr in bytecode)

def test_integration_with_python(framework):
    code = "చేపాయిపిండి('హలో, ప్రపంచం!')"
    result = framework.run(code, mode='interpret')
    assert result == 'హలో, ప్రపంచం!'

def test_core_libraries(framework):
    # Test math operations
    code = "చర result = గణితం.పవర్(2, 3)"
    result = framework.run(code, mode='interpret')
    assert result == 8

    # Test string manipulation
    code = "చర text = 'హలో'.చేర్చు(' ప్రపంచం')"
    result = framework.run(code, mode='interpret')
    assert result == 'హలో ప్రపంచం'

    # Test file I/O
    code = """
    ఫైల్.వ్రాయి('test.txt', 'హలో, ప్రపంచం!')
    చర content = ఫైల్.చదువు('test.txt')
    చేపాయిపిండి(content)
    """
    result = framework.run(code, mode='interpret')
    assert result == 'హలో, ప్రపంచం!'

    # Test data structures
    code = """
    చర జాబితా = [1, 2, 3]
    జాబితా.చేర్చు(4)
    చేపాయిపిండి(జాబితా)
    """
    result = framework.run(code, mode='interpret')
    assert result == [1, 2, 3, 4]
