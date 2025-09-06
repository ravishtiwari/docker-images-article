
#!/bin/bash

# Script to run tests with different configurations

echo "Running IMDb API Test Suite"
echo "=========================="

# Set environment variables for testing
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DATABASE_URL="sqlite:///./test.db"

# Function to run tests with specific options
run_tests() {
    local test_type=$1
    local options=$2
    
    echo ""
    echo "Running $test_type tests..."
    echo "----------------------------"
    
    if pytest $options; then
        echo "✅ $test_type tests passed"
    else
        echo "❌ $test_type tests failed"
        exit 1
    fi
}

# Clean up any existing test artifacts
echo "Cleaning up test artifacts..."
rm -f test.db
rm -rf htmlcov/
rm -f .coverage

# Run different test suites
run_tests "Unit" "tests/ -m 'not integration and not slow' -v"
run_tests "Integration" "tests/ -m integration -v"
run_tests "All" "tests/ -v --cov=app --cov-report=term-missing --cov-report=html"

echo ""
echo "=========================="
echo "All tests completed successfully! 🎉"
echo ""
echo "Coverage report generated in htmlcov/index.html"
echo "Open it in your browser to view detailed coverage information."
