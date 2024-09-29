import ctypes
from llvmlite import ir
from llvmlite import binding as llvm
from telugu_parser import TeluguParser, NumberNode, BinOpNode, AssignNode, VariableNode, PrintNode, IfNode, StringNode
from telugu_lexer import TeluguLexer
from telugu_parser import parser
from telugu_lexer import lexer

class TeluguCompiler:
    def __init__(self):
        self.module = ir.Module(name="telugu_module")
        self.builder = None
        self.printf = None
        self.variables = {}

    def _create_execution_engine(self):
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
        return engine

    def _declare_print_function(self):
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        return printf

    def _compile_number(self, node):
        return ir.Constant(ir.DoubleType(), float(node.value))

    def _compile_string(self, node):
        string = node.value
        c_str_type = ir.ArrayType(ir.IntType(8), len(string) + 1)
        global_str = ir.GlobalVariable(self.module, c_str_type, name=f"str_{len(self.module.global_variables)}")
        global_str.global_constant = True
        global_str.initializer = ir.Constant(c_str_type, bytearray(string.encode('utf8') + b'\00'))
        return global_str

    def _compile_binop(self, node):
        left = self.compile(node.left)
        right = self.compile(node.right)
        if node.op == '+':
            return self.builder.fadd(left, right)
        elif node.op == '-':
            return self.builder.fsub(left, right)
        elif node.op == '*':
            return self.builder.fmul(left, right)
        elif node.op == '/':
            return self.builder.fdiv(left, right)
        elif node.op == '>':
            return self.builder.fcmp_ordered('>', left, right)
        elif node.op == '<':
            return self.builder.fcmp_ordered('<', left, right)

    def _compile_assign(self, node):
        value = self.compile(node.value)
        var_addr = self.builder.alloca(ir.DoubleType(), name=node.name)
        self.builder.store(value, var_addr)
        self.variables[node.name] = var_addr
        return value

    def _compile_variable(self, node):
        return self.builder.load(self.variables[node.name])

    def _compile_print(self, node):
        value = self.compile(node.value)
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%f\n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])

    def _compile_if(self, node):
        condition = self.compile(node.condition)
        with self.builder.if_else(condition) as (then, otherwise):
            with then:
                self.compile(node.true_body)
            with otherwise:
                if node.false_body:
                    self.compile(node.false_body)

    def compile(self, node):
        if isinstance(node, NumberNode):
            return self._compile_number(node)
        elif isinstance(node, StringNode):
            return self._compile_string(node)
        elif isinstance(node, BinOpNode):
            return self._compile_binop(node)
        elif isinstance(node, AssignNode):
            return self._compile_assign(node)
        elif isinstance(node, VariableNode):
            return self._compile_variable(node)
        elif isinstance(node, PrintNode):
            return self._compile_print(node)
        elif isinstance(node, IfNode):
            return self._compile_if(node)

    def compile_ir(self, code):
        lexer = TeluguLexer()
        parser = TeluguParser()
        tokens = lexer.tokenize(code)
        ast = parser.parse(tokens)

        # Initialize the module and builder
        self.module = ir.Module(name="telugu_module")
        self.builder = ir.IRBuilder()

        # Declare the printf function
        self.printf = self._declare_print_function()

        # Define and start the main function
        main_ty = ir.FunctionType(ir.IntType(32), [])
        main = ir.Function(self.module, main_ty, name="main")
        block = main.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # Compile the AST
        self.compile(ast)

        # Add a return statement to the main function
        self.builder.ret(ir.Constant(ir.IntType(32), 0))

        return str(self.module)

    def compile_and_run(self, code):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        ir_code = self.compile_ir(code)

        # Create an execution engine
        engine = self._create_execution_engine()

        # Add the IR to the engine and finalize it
        mod = llvm.parse_assembly(ir_code)
        mod.verify()
        engine.add_module(mod)
        engine.finalize_object()

        # Run the code
        engine.run_static_constructors()
        func_ptr = engine.get_function_address("main")

        # Convert the pointer to a Python function and call it
        cfunc = ctypes.CFUNCTYPE(ctypes.c_int)(func_ptr)
        result = cfunc()

        return result

if __name__ == "__main__":
    compiler = TeluguCompiler()

    test_code = '''
    చర సంఖ్య = 10
    చేపాయిపిండి(సంఖ్య)

    యెడల (సంఖ్య > 5) {
        చేపాయిపిండి("సంఖ్య పెద్దది 5 కంటే")
    } లేక {
        చేపాయిపిండి("సంఖ్య చిన్నది లేదా సమానం 5కి")
    }
    '''

    print("Compiled IR:")
    print(compiler.compile_ir(test_code))

    print("\nRunning compiled code:")
    compiler.compile_and_run(test_code)
