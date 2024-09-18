#!/bin/bash

# TeluguFusion Integration Test Runner

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

# Main integration test runner
main() {
    local test_dir="$TELUGUFUSION_HOME/tests"
    local failed_tests=0

    # Unicode support test
    run_test "$test_dir/unicode_support_test.tel" "యూనికోడ్ మద్దతు పరీక్ష విజయవంతమైంది"
    failed_tests=$((failed_tests + $?))

    # Mathematical operations test
    run_test "$test_dir/math_operations_test.tel" "గణిత పరిక్రియల పరీక్ష విజయవంతమైంది"
    failed_tests=$((failed_tests + $?))

    # Web features test
    run_test "$test_dir/web_features_test.tel" "వెబ్ లక్షణాల పరీక్ష విజయవంతమైంది"
    failed_tests=$((failed_tests + $?))

    # Localization features test
    run_test "$test_dir/localization_test.tel" "స్థానికీకరణ లక్షణాల పరీక్ష విజయవంతమైంది"
    failed_tests=$((failed_tests + $?))

    # Component interaction test
    run_test "$test_dir/component_interaction_test.tel" "భాగాల అంతర్ క్రియ పరీక్ష విజయవంతమైంది"
    failed_tests=$((failed_tests + $?))

    # Print final results
    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}All integration tests passed successfully!${NC}"
    else
        echo -e "${RED}$failed_tests integration test(s) failed.${NC}"
    fi

    exit $failed_tests
}

# Run the main function
main
