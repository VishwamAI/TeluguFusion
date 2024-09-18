#!/bin/bash

# TeluguFusion Deployment Script

set -e

# Configuration
PROJECT_ROOT="/home/ubuntu/TeluguFusion"
BUILD_DIR="$PROJECT_ROOT/build"
INSTALL_DIR="/usr/local/telugufusion"
COMPILER_SRC="$PROJECT_ROOT/src/compiler_main.tel"
INTERPRETER_SRC="$PROJECT_ROOT/src/interpreter_main.tel"

# Check for existing TeluguFusion installation
if command -v telugufusion &> /dev/null; then
    echo "TeluguFusion is already installed. Updating..."
    UPDATING=true
else
    echo "TeluguFusion not found. Proceeding with fresh installation..."
    UPDATING=false
fi

# Create build directory
mkdir -p "$BUILD_DIR"

# Create a temporary Python script for initial compilation
echo "Creating temporary Telugu to C++ converter..."
cat << EOF > "$BUILD_DIR/telugu_to_cpp.py"
#!/usr/bin/env python3
import sys

def convert_telugu_to_cpp(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        telugu_code = f.read()

    # Basic Telugu to C++ conversion logic
    cpp_code = """// Converted from Telugu
#include <iostream>
#include <string>
#include <codecvt>
#include <locale>
#include <vector>
#include <list>
#include <map>
#include <memory>

std::wstring_convert<std::codecvt_utf8<wchar_t>> utf8_conv;

template<typename T>
void అభ్యర్థించు(T condition, const std::string& message) {
    if (!condition) {
        std::wcerr << utf8_conv.from_bytes("అభ్యర్థన విఫలమైంది: ") << utf8_conv.from_bytes(message) << std::endl;
        std::exit(1);
    }
}

"""

    # Convert Telugu keywords and data types to C++ equivalents
    keyword_map = {
        # Basic keywords
        "ప్రమేయం": "auto",
        "చర": "auto",
        "తిరిగిఇవ్వు": "return",
        "ఒకవేళ": "if",
        "లేకపోతే": "else",
        "అయ్యేవరకు": "while",
        "కొరకు": "for",
        "నిజం": "true",
        "తప్పు": "false",

        # Class-related keywords
        "తరగతి": "class",
        "ప్రజా": "public",
        "ప్రైవేట్": "private",
        "రక్షిత": "protected",
        "వర్చువల్": "virtual",
        "అమూర్త": "abstract",
        "ఓవర్రైడ్": "override",
        "స్థిర": "static",
        "నమూనా": "template",
        "రకం": "typename",
        "ఆటో": "auto",
        "నూతన": "new",
        "తొలగించు": "delete",
        "ఈ": "this",
        "సూపర్": "super",
        "ఇంటర్ఫేస్": "class",
        "అమలు": "implements",
        "విస్తరించు": "extends",

        # Data types
        "పూర్ణం": "int",
        "తేలియాడు": "float",
        "డబుల్": "double",
        "వాక్యం": "std::wstring",
        "బూలియన్": "bool",
        "శూన్యం": "void",
        "చార్": "char",
        "లాంగ్": "long",
        "షార్ట్": "short",
        "అన్సైన్డ్": "unsigned",
        "సైజ్_టి": "size_t",

        # Modifiers
        "స్థిరం": "const",
        "ఎనుమ్": "enum",
        "మూలం": "mutable",
        "నిర్దిష్ట": "explicit",
        "ఇన్లైన్": "inline",

        # Data structures
        "వెక్టర్": "std::vector",
        "జాబితా": "std::list",
        "నిఘంటువు": "std::map",
        "జత": "std::pair",
        "క్యూ": "std::queue",
        "స్టాక్": "std::stack",
        "సెట్": "std::set",
        "జ్ఞాపకం": "std::shared_ptr",
        "యూనీక్_జ్ఞాపకం": "std::unique_ptr",
        "అసంఘటిత_నిఘంటువు": "std::unordered_map",
        "అసంఘటిత_సెట్": "std::unordered_set",
        "అనుకూల_జాబితా": "std::array",

        # I/O and system
        "దిగుమతి": "#include",
        "వ్యవస్థ": "std",
        "బయటకు": "cout",
        "లోపలికి": "cin",
        "దోష_ప్రవాహం": "cerr",
        "ముగింపుపంక్తి": "endl",
        "ఫైల్_ప్రవాహం": "fstream",

        # Control flow
        "స్విచ్": "switch",
        "కేసు": "case",
        "డిఫాల్ట్": "default",
        "విరామం": "break",
        "కొనసాగించు": "continue",
        "గోటు": "goto",

        # Exception handling
        "ప్రయత్నించు": "try",
        "పట్టుకో": "catch",
        "చివరగా": "finally",
        "దోషం_విసురు": "throw",
        "మినహాయింపు": "exception",

        # Operators
        "మరియు": "&&",
        "లేదా": "||",
        "కాదు": "!",
        "సభ్యుడు": "->",
        "పరిమాణం": "sizeof",
        "కొత్త": "new",
        "కొత్త[]": "new[]",
        "తొలగించు": "delete",
        "తొలగించు[]": "delete[]",

        # Punctuation and other symbols
        ";": ";",
        ",": ",",
        ".": ".",
        "(": "(",
        ")": ")",
        "{": "{",
        "}": "}",
        "[": "[",
        "]": "]",
        "<": "<",
        ">": ">",
        "=": "=",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
        "%": "%",
        "&": "&",
        "|": "|",
        "^": "^",
        "~": "~",
        "::": "::",
        "?": "?",
        ":": ":",
        "<<": "<<",
        ">>": ">>",
    }

    for telugu, cpp in keyword_map.items():
        telugu_code = telugu_code.replace(telugu, cpp)

    # Add main function
    cpp_code += "int main() {\n"

    # Convert Telugu code to C++
    indent_level = 0
    for line in telugu_code.split('\n'):
        line = line.strip()
        if line.startswith("//"):
            cpp_code += f"{'    ' * indent_level}{line}\n"
        elif line.startswith("/*"):
            cpp_code += f"{'    ' * indent_level}{line}\n"
            indent_level += 1
        elif line.startswith("*/"):
            indent_level -= 1
            cpp_code += f"{'    ' * indent_level}{line}\n"
        elif line.startswith("తరగతి"):
            class_parts = line.split()
            class_name = class_parts[1]
            inheritance = ""
            if len(class_parts) > 2 and class_parts[2] == "వారసత్వం":
                inheritance = f" : public {class_parts[3]}"
            cpp_code += f"{'    ' * indent_level}class {class_name}{inheritance} {{\n"
            indent_level += 1
        elif line.startswith("ప్రజా:") or line.startswith("ప్రైవేట్:") or line.startswith("రక్షిత:"):
            access_specifier = "public" if line.startswith("ప్రజా:") else "private" if line.startswith("ప్రైవేట్:") else "protected"
            cpp_code += f"{'    ' * indent_level}{access_specifier}:\n"
        elif line.startswith("ప్రమేయం"):
            func_parts = line.split()
            func_name = func_parts[1].split('(')[0]
            params = line.split('(')[1].split(')')[0]
            return_type = "auto"
            if "->" in line:
                return_type = line.split("->")[1].strip()
            cpp_code += f"{'    ' * indent_level}{return_type} {func_name}({params}) {{\n"
            indent_level += 1
        elif line == "}":
            indent_level -= 1
            cpp_code += f"{'    ' * indent_level}}}\n"
        elif "వ్యవస్థ.బయటకు.వ్రాయు" in line:
            output = line.split("వ్యవస్థ.బయటకు.వ్రాయు(")[1].split(")")[0]
            cpp_code += f"{'    ' * indent_level}std::wcout << utf8_conv.from_bytes({output}) << std::endl;\n"
        elif "అభ్యర్థించు" in line:
            condition, message = line.split("అభ్యర్థించు(")[1].split(", ")
            cpp_code += f"{'    ' * indent_level}assert({condition.strip()}, {message.strip()[:-1]});\n"
        elif any(keyword in line for keyword in ["ఒకవేళ", "లేకపోతే", "అయ్యేవరకు", "కొరకు"]):
            cpp_line = line
            for telugu, cpp in keyword_map.items():
                cpp_line = cpp_line.replace(telugu, cpp)
            cpp_code += f"{'    ' * indent_level}{cpp_line}\n"
        else:
            cpp_line = line
            for telugu, cpp in keyword_map.items():
                cpp_line = cpp_line.replace(telugu, cpp)
            cpp_code += f"{'    ' * indent_level}{cpp_line}\n"

    cpp_code += "    return 0;\n}\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cpp_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python telugu_to_cpp.py input_file output_file")
        sys.exit(1)
    convert_telugu_to_cpp(sys.argv[1], sys.argv[2])
EOF
chmod +x "$BUILD_DIR/telugu_to_cpp.py"

# Convert Telugu source to C++
echo "Converting TeluguFusion compiler source to C++..."
python3 "$BUILD_DIR/telugu_to_cpp.py" "$COMPILER_SRC" "$BUILD_DIR/telugufusion_compiler.cpp"

echo "Converting TeluguFusion interpreter source to C++..."
python3 "$BUILD_DIR/telugu_to_cpp.py" "$INTERPRETER_SRC" "$BUILD_DIR/telugufusion_interpreter.cpp"

# Compile C++ code to executables
echo "Compiling TeluguFusion compiler..."
g++ -std=c++17 -O2 "$BUILD_DIR/telugufusion_compiler.cpp" -o "$BUILD_DIR/telugufusion_compiler"

echo "Compiling TeluguFusion interpreter..."
g++ -std=c++17 -O2 "$BUILD_DIR/telugufusion_interpreter.cpp" -o "$BUILD_DIR/telugufusion-interpreter"

# Install TeluguFusion
echo "Installing TeluguFusion..."
sudo mkdir -p "$INSTALL_DIR"

# Compile the generated C++ code for the compiler
echo "Compiling TeluguFusion compiler..."
g++ -std=c++17 -O2 "$BUILD_DIR/telugufusion_compiler.cpp" -o "$BUILD_DIR/telugufusion"

# Compile the generated C++ code for the interpreter
echo "Compiling TeluguFusion interpreter..."
g++ -std=c++17 -O2 "$BUILD_DIR/telugufusion_interpreter.cpp" -o "$BUILD_DIR/telugufusion-interpreter"

# Install the compiled binaries
sudo cp "$BUILD_DIR/telugufusion" "$INSTALL_DIR/"
sudo cp "$BUILD_DIR/telugufusion-interpreter" "$INSTALL_DIR/"

# Set execute permissions
sudo chmod +x "$INSTALL_DIR/telugufusion"
sudo chmod +x "$INSTALL_DIR/telugufusion-interpreter"

# Add TeluguFusion to PATH
if [ "$UPDATING" = false ]; then
    echo "export PATH=\$PATH:$INSTALL_DIR" | sudo tee -a /etc/profile.d/telugufusion.sh
fi

# Generate documentation
echo "Generating documentation..."
"$INSTALL_DIR/telugufusion" "$PROJECT_ROOT/src/doc_generator.tel" "$PROJECT_ROOT/docs" -o "$INSTALL_DIR/docs"

# Set up development environment
echo "Setting up development environment..."
pip install -r "$PROJECT_ROOT/requirements.txt"

# Create contribution guidelines
echo "Creating contribution guidelines..."
cat << EOF > "$PROJECT_ROOT/CONTRIBUTING.md"
# Contributing to TeluguFusion

We welcome contributions to TeluguFusion! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with a clear commit message
4. Push your changes to your fork
5. Create a pull request with a description of your changes

For more detailed information, please refer to our [documentation](docs/contributing.md).
EOF

echo "TeluguFusion has been successfully deployed and set up for development!"
echo "Please restart your terminal or run 'source /etc/profile.d/telugufusion.sh' to use TeluguFusion."
