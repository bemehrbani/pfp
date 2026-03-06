#!/bin/bash

# Test runner script for People for Peace Campaign Manager
# This script provides various options for running the test suite

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Default values
DOCKER_COMPOSE_FILE="docker-compose.yml"
BACKEND_SERVICE="backend"
TEST_COMMAND="python manage.py test"
COVERAGE_COMMAND="coverage run manage.py test"
COVERAGE_REPORT="coverage report"
COVERAGE_HTML="coverage html"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -h, --help           Show this help message"
            echo "  -a, --all            Run all tests (default)"
            echo "  -u, --users          Run only users app tests"
            echo "  -c, --campaigns      Run only campaigns app tests"
            echo "  -t, --tasks          Run only tasks app tests"
            echo "  -l, --analytics      Run only analytics app tests"
            echo "  -g, --telegram       Run only telegram app tests"
            echo "  --coverage           Run tests with coverage report"
            echo "  --coverage-html      Generate HTML coverage report"
            echo "  --no-docker          Run tests directly (not in Docker)"
            echo "  --verbose            Show verbose test output"
            echo ""
            exit 0
            ;;
        -a|--all)
            TEST_APPS=""
            shift
            ;;
        -u|--users)
            TEST_APPS="apps.users"
            shift
            ;;
        -c|--campaigns)
            TEST_APPS="apps.campaigns"
            shift
            ;;
        -t|--tasks)
            TEST_APPS="apps.tasks"
            shift
            ;;
        -l|--analytics)
            TEST_APPS="apps.analytics"
            shift
            ;;
        -g|--telegram)
            TEST_APPS="apps.telegram"
            shift
            ;;
        --coverage)
            USE_COVERAGE=true
            shift
            ;;
        --coverage-html)
            USE_COVERAGE=true
            GENERATE_HTML=true
            shift
            ;;
        --no-docker)
            USE_DOCKER=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set defaults if not specified
TEST_APPS=${TEST_APPS:-""}
USE_COVERAGE=${USE_COVERAGE:-false}
GENERATE_HTML=${GENERATE_HTML:-false}
USE_DOCKER=${USE_DOCKER:-true}
VERBOSE=${VERBOSE:-false}

# Build test command
if [ -n "$TEST_APPS" ]; then
    TEST_CMD="$TEST_COMMAND $TEST_APPS"
    COVERAGE_CMD="$COVERAGE_COMMAND $TEST_APPS"
else
    TEST_CMD="$TEST_COMMAND"
    COVERAGE_CMD="$COVERAGE_COMMAND"
fi

# Add verbose flag if requested
if [ "$VERBOSE" = true ]; then
    TEST_CMD="$TEST_CMD -v 2"
    COVERAGE_CMD="$COVERAGE_CMD -v 2"
fi

run_tests_in_docker() {
    print_header "Running tests in Docker container"

    if [ "$USE_COVERAGE" = true ]; then
        print_info "Running tests with coverage..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T "$BACKEND_SERVICE" bash -c "$COVERAGE_CMD"

        if [ $? -eq 0 ]; then
            print_success "Tests passed!"

            # Generate coverage report
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T "$BACKEND_SERVICE" bash -c "$COVERAGE_REPORT"

            if [ "$GENERATE_HTML" = true ]; then
                print_info "Generating HTML coverage report..."
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T "$BACKEND_SERVICE" bash -c "$COVERAGE_HTML"
                print_success "HTML coverage report generated in htmlcov/"
            fi
        else
            print_error "Tests failed!"
            exit 1
        fi
    else
        print_info "Running tests..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T "$BACKEND_SERVICE" bash -c "$TEST_CMD"

        if [ $? -eq 0 ]; then
            print_success "All tests passed!"
        else
            print_error "Tests failed!"
            exit 1
        fi
    fi
}

run_tests_directly() {
    print_header "Running tests directly"

    # Check if we're in the right directory
    if [ ! -f "manage.py" ]; then
        print_error "manage.py not found. Please run from the project root directory."
        exit 1
    fi

    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        print_info "Activating virtual environment..."
        source venv/bin/activate
    fi

    # Install coverage if needed
    if [ "$USE_COVERAGE" = true ]; then
        if ! command -v coverage &> /dev/null; then
            print_info "Installing coverage..."
            pip install coverage
        fi
    fi

    # Install test dependencies
    print_info "Installing test dependencies..."
    pip install -r requirements.txt

    # Run tests
    if [ "$USE_COVERAGE" = true ]; then
        print_info "Running tests with coverage..."
        $COVERAGE_CMD

        if [ $? -eq 0 ]; then
            print_success "Tests passed!"

            # Generate coverage report
            $COVERAGE_REPORT

            if [ "$GENERATE_HTML" = true ]; then
                print_info "Generating HTML coverage report..."
                $COVERAGE_HTML
                print_success "HTML coverage report generated in htmlcov/"
            fi
        else
            print_error "Tests failed!"
            exit 1
        fi
    else
        print_info "Running tests..."
        $TEST_CMD

        if [ $? -eq 0 ]; then
            print_success "All tests passed!"
        else
            print_error "Tests failed!"
            exit 1
        fi
    fi
}

# Main execution
if [ "$USE_DOCKER" = true ]; then
    # Check if Docker Compose is running
    if ! docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "Up"; then
        print_error "Docker Compose services are not running. Starting them..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

        # Wait for services to be ready
        print_info "Waiting for services to be ready..."
        sleep 10
    fi

    run_tests_in_docker
else
    run_tests_directly
fi

print_header "Test run completed"