#!/bin/bash

# Check if main.cpp exists
if [ ! -f "main.cpp" ]; then
    echo "Error: main.cpp not found in the current directory."
    exit 1
fi

# Add #include "utils.h" at the beginning of main.cpp
sed -i '1i#include "utils.h"' main.cpp

echo "Added #include \"utils.h\" to main.cpp"
