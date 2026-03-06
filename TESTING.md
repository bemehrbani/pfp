# Comprehensive Test Suite for People for Peace Campaign Manager

This document describes the comprehensive test suite created for the People for Peace Campaign Manager backend.

## Overview

The test suite provides complete coverage of all Django models, API endpoints, and signal handlers across all 5 apps:

1. **Users App** (`/backend/apps/users/tests.py`)
2. **Campaigns App** (`/backend/apps/campaigns/tests.py`)
3. **Tasks App** (`/backend/apps/tasks/tests.py`)
4. **Analytics App** (`/backend/apps/analytics/tests.py`)
5. **Telegram App** (`/backend/apps/telegram/tests.py`)

## Test Structure

Each test file follows a consistent structure:

### 1. Model Tests
- Test model creation with all fields
- Test model methods and properties
- Test string representations
- Test indexes and constraints
- Test edge cases and validation

### 2. API Tests
- Test all CRUD operations
- Test authentication and authorization
- Test success and error responses
- Test permission checks by role
- Test data validation

### 3. Signal Tests
- Test signal handlers for model events
- Test ActivityLog creation for audit trails
- Test state transitions and side effects

## Running Tests

### Using Docker (Recommended)

```bash
# Make the test runner script executable
chmod +x run_tests.sh

# Run all tests
./run_tests.sh

# Run tests with coverage report
./run_tests.sh --coverage

# Run tests with HTML coverage report
./run_tests.sh --coverage-html

# Run tests for specific app
./run_tests.sh --users      # Users app only
./run_tests.sh --campaigns  # Campaigns app only
./run_tests.sh --tasks      # Tasks app only
./run_tests.sh --analytics  # Analytics app only
./run_tests.sh --telegram   # Telegram app only

# Run with verbose output
./run_tests.sh --verbose

# Run directly (not in Docker)
./run_tests.sh --no-docker
```

### Using Docker Compose Directly

```bash
# Run all tests
docker-compose exec backend python manage.py test

# Run specific app tests
docker-compose exec backend python manage.py test apps.users
docker-compose exec backend python manage.py test apps.campaigns
docker-compose exec backend python manage.py test apps.tasks
docker-compose exec backend python manage.py test apps.analytics
docker-compose exec backend python manage.py test apps.telegram

# Run with coverage
docker-compose exec backend coverage run manage.py test
docker-compose exec backend coverage report
docker-compose exec backend coverage html  # Generate HTML report
```

### Manual Execution

```bash
# Navigate to backend directory
cd backend

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.campaigns
python manage.py test apps.tasks
python manage.py test apps.analytics
python manage.py test apps.telegram
```

## Test Coverage

### Users App Tests
- **User Model Tests**: Creation, role methods, level updates, Telegram fields
- **User API Tests**: Registration, login, profile, Telegram linking, password change
- **Signal Tests**: User creation/update, Telegram linking, login/logout events

### Campaigns App Tests
- **Campaign Model Tests**: Creation, progress calculation, status methods
- **CampaignVolunteer Model Tests**: Volunteer enrollment, status tracking
- **CampaignUpdate Model Tests**: Announcements and updates
- **Campaign API Tests**: CRUD operations, volunteer joining, statistics
- **Signal Tests**: Campaign creation, volunteer joining, manager changes

### Tasks App Tests
- **Task Model Tests**: Creation, availability checking, slot calculation
- **TaskAssignment Model Tests**: Status transitions, points awarding
- **Task API Tests**: CRUD operations, assignment, completion, verification
- **Signal Tests**: Task creation, assignment status changes, points updates

### Analytics App Tests
- **ActivityLog Model Tests**: Creation with different action types, metadata
- **AnalyticsSnapshot Model Tests**: Snapshot creation, unique constraints
- **Analytics API Tests**: Dashboard stats, campaign analytics, system analytics
- **Permission Tests**: Role-based access to analytics data

### Telegram App Tests
- **TelegramSession Model Tests**: Creation, state management, command tracking
- **TelegramMessageLog Model Tests**: Message logging, audit trails
- **Telegram API Tests**: Webhook handling, bot status, message sending
- **Mock Tests**: External API mocking for Telegram bot interactions

## Test Data and Fixtures

All tests use Django's `setUp()` method to create test data:
- Test users with different roles (admin, campaign_manager, volunteer)
- Test campaigns with various statuses and types
- Test tasks with different assignment types
- Test assignments with different statuses
- Test activity logs for audit trails

## Mocking External Dependencies

The test suite properly mocks external dependencies:
- **Telegram API**: All Telegram bot interactions are mocked
- **External Services**: Any external API calls are mocked
- **File Operations**: File uploads and storage operations are mocked

## Test Isolation

All tests are properly isolated:
- Use Django's TestCase and APITestCase with transaction support
- Each test runs in its own transaction
- Test data is cleaned up after each test
- No test depends on another test's data

## Best Practices Followed

1. **Comprehensive Coverage**: Tests cover models, APIs, and signals
2. **Role-Based Testing**: Tests verify permissions for different user roles
3. **Edge Cases**: Tests include error conditions and boundary cases
4. **Readable Tests**: Clear test names and assertions
5. **Fast Execution**: Tests run quickly with proper mocking
6. **No External Dependencies**: Tests don't require external services

## Test Output

When tests run successfully, you'll see output like:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................
----------------------------------------------------------------------
Ran 25 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Ensure Docker containers are running: `docker-compose up -d`
   - Check database migrations: `docker-compose exec backend python manage.py migrate`

2. **Test Failures**:
   - Check test output for specific error messages
   - Verify test data setup in `setUp()` methods
   - Ensure all required models are imported

3. **Coverage Issues**:
   - Install coverage: `pip install coverage`
   - Run coverage with proper command: `coverage run manage.py test`

### Debugging Tests

To debug a specific test:
```bash
# Run a single test class
python manage.py test apps.users.tests.UserModelTests

# Run a single test method
python manage.py test apps.users.tests.UserModelTests.test_user_creation

# Run with pdb (Python debugger)
python -m pdb manage.py test apps.users
```

## Adding New Tests

When adding new features, follow these patterns:

1. **Add Model Tests** for any new models
2. **Add API Tests** for any new endpoints
3. **Add Signal Tests** for any new signal handlers
4. **Update Existing Tests** if functionality changes

## Continuous Integration

For CI/CD integration, the test suite can be run with:

```yaml
# Example GitHub Actions configuration
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          docker-compose up -d
          docker-compose exec -T backend python manage.py test
```

## Coverage Reports

To generate coverage reports:
```bash
# Generate text report
coverage report

# Generate HTML report (opens in browser)
coverage html
open htmlcov/index.html

# Generate XML report for CI tools
coverage xml
```

The coverage report shows which lines of code are covered by tests, helping identify areas that need more testing.