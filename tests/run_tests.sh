#!/bin/bash

# TeluguFusion Test Runner

# Set up environment
export TELUGUFUSION_HOME="/home/ubuntu/TeluguFusion"
export PATH="$TELUGUFUSION_HOME/bin:$PATH"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to run a test and check its output
run_test() {
    local test_file="$1"
    local expected_output="$2"

    echo "Running test: $test_file"

    # Run the test file using the TeluguFusion interpreter
    output=$(telugufusion-interpreter "$test_file" 2>&1)

    # Check if the output matches the expected output
    if [[ "$output" == *"$expected_output"* ]]; then
        echo -e "${GREEN}Test passed: $test_file${NC}"
        return 0
    else
        echo -e "${RED}Test failed: $test_file${NC}"
        echo "Expected output: $expected_output"
        echo "Actual output: $output"
        return 1
    fi
}

# Main test runner
main() {
    local test_dir="$TELUGUFUSION_HOME/tests"
    local failed_tests=0

    # Run comprehensive tests
    run_test "$test_dir/comprehensive_tests.tel" "Hello from TeluguFusion!"
    failed_tests=$((failed_tests + $?))

    # Add more specific tests here
    # For example:
    # run_test "$test_dir/type_system_tests.tel" "రకాల వ్యవస్థ పరీక్షలు విజయవంతమైనాయి"
    # failed_tests=$((failed_tests + $?))

    # Print final results
    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}All tests passed successfully!${NC}"
    else
        echo -e "${RED}$failed_tests test(s) failed.${NC}"
    fi

    exit $failed_tests
}

# Run the main function
main
