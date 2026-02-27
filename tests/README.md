# Testing Documentation

Comprehensive test suite for the Mergington High School Activities FastAPI application.

## Overview

This test suite provides thorough coverage of the API endpoints with both integration and unit tests. The tests verify correct behavior for success scenarios, error handling, state management, and data structure integrity.

## Test Structure

```
tests/
├── __init__.py           # Python package initialization
├── conftest.py           # Shared pytest fixtures and configuration
├── test_integration.py   # Integration tests for API endpoints
├── test_unit.py          # Unit tests for data structures and components
└── README.md             # This file
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_integration.py
pytest tests/test_unit.py

# Run specific test class
pytest tests/test_integration.py::TestGetActivities

# Run specific test function
pytest tests/test_integration.py::TestActivitySignup::test_signup_success

# Run tests by marker
pytest -m integration
pytest -m unit
```

### Coverage Reports

```bash
# Run with coverage (configured in pytest.ini)
pytest --cov=src --cov-report=html --cov-report=term-missing

# Generate only HTML report
pytest --cov=src --cov-report=html

# Generate only terminal report
pytest --cov=src --cov-report=term
```

### Watch Mode (with pytest-watch)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests automatically on file changes
ptw
```

## Test Files

### `conftest.py`

Contains shared pytest fixtures used across all test files:

- **`client`** - FastAPI TestClient instance for making HTTP requests
- **`reset_activities`** - Automatically resets in-memory activities data after each test (critical for test isolation)
- **`sample_emails`** - List of test email addresses for signup/unregister operations
- **`activity_names`** - List of all valid activity names for parametrized tests  
- **`filled_activity`** - Pre-configured activity at maximum capacity for testing "activity full" scenarios

### `test_integration.py`

Integration tests that exercise full API endpoints:

#### TestGetActivities
- List all activities with correct structure
- Verify all 9 activities are present
- Check initial state (empty participants)

#### TestActivitySignup
- ✅ Successful signup
- ✅ URL encoding for activity names with spaces
- ✅ Multiple students signing up for same activity
- ❌ Activity not found (404)
- ❌ Already registered (400)
- ❌ Activity full (400)
- Parametrized tests for multiple activities

#### TestActivityUnregister
- ✅ Successful unregister
- ✅ URL encoding support
- ❌ Activity not found (404)
- ❌ Participant not found (404)
- Verify correct participant removal

#### TestRootEndpoint
- Root redirect functionality

#### TestStateManagement
- Complete signup/unregister workflow
- State isolation between tests
- Multiple operations in sequence

### `test_unit.py`

Unit tests for isolated components and data structures:

#### TestActivitiesDataStructure
- Activities dictionary initialization
- Correct number of activities (9)
- Required fields present
- Field type validation
- Data constraints (positive max_participants, non-empty strings)
- Parametrized tests for specific activity configurations

#### TestActivityNames
- All expected activities exist
- Activity names are valid strings
- No empty activity names

#### TestParticipantsListOperations
- List mutability (add/remove operations)
- Duplicate detection
- Basic list operations

## Fixtures Explained

### `client` Fixture

Provides a FastAPI TestClient for making HTTP requests to the API:

```python
def test_example(client):
    response = client.get("/activities")
    assert response.status_code == 200
```

### `reset_activities` Fixture (Auto-use)

**Critical for test isolation!** This fixture automatically runs after every test to reset the in-memory `activities` dictionary to its original state. Without this, tests would interfere with each other.

You don't need to explicitly use this fixture - it runs automatically via `autouse=True`.

### `sample_emails` Fixture

Provides test email addresses:

```python
def test_signup(client, sample_emails):
    email = sample_emails[0]  # "student1@school.edu"
    response = client.post(f"/activities/Chess Club/signup", params={"email": email})
```

### `activity_names` Fixture

List of all valid activity names for parametrized tests:

```python
@pytest.mark.parametrize("activity_name", activity_names)
def test_all_activities(client, activity_name):
    # Test runs for each activity
    pass
```

### `filled_activity` Fixture

Creates an activity at maximum capacity for testing "activity full" scenarios:

```python
def test_full_activity(client, filled_activity):
    activity_name = filled_activity["name"]
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "new@school.edu"}
    )
    assert response.status_code == 400  # Activity is full
```

## Writing New Tests

### Integration Test Example

```python
@pytest.mark.integration
def test_my_new_feature(client, sample_emails):
    """Test description here."""
    # Arrange
    email = sample_emails[0]
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
```

### Unit Test Example

```python
@pytest.mark.unit
def test_data_structure():
    """Test description here."""
    from src.app import activities
    
    assert "Chess Club" in activities
    assert activities["Chess Club"]["max_participants"] == 20
```

### Parametrized Test Example

```python
@pytest.mark.parametrize("activity_name,email", [
    ("Chess Club", "test1@school.edu"),
    ("Programming Club", "test2@school.edu"),
    ("Art Studio", "test3@school.edu"),
])
def test_signup_multiple_activities(client, activity_name, email):
    """Test signup works for different activities."""
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
```

## Best Practices

### 1. Use Descriptive Test Names

✅ Good: `test_signup_activity_not_found_returns_404`  
❌ Bad: `test_signup_error`

### 2. Follow AAA Pattern

```python
def test_example(client):
    # Arrange - Set up test data
    email = "test@school.edu"
    
    # Act - Perform the action
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Assert - Verify the result
    assert response.status_code == 200
```

### 3. Test One Thing Per Test

Each test should verify a single behavior or scenario.

### 4. Use Fixtures for Reusability

Don't repeat setup code - use fixtures defined in `conftest.py`.

### 5. Mark Tests Appropriately

```python
@pytest.mark.integration  # For endpoint tests
@pytest.mark.unit         # For isolated component tests
```

### 6. Handle URL Encoding

Activity names with spaces need URL encoding:

```python
from urllib.parse import quote

activity_name = "Chess Club"
encoded_name = quote(activity_name)  # "Chess%20Club"
response = client.post(f"/activities/{encoded_name}/signup", ...)
```

### 7. Verify State Changes

When testing signup/unregister, verify the state actually changed:

```python
# Sign up
client.post("/activities/Chess Club/signup", params={"email": email})

# Verify participant was actually added
response = client.get("/activities")
assert email in response.json()["Chess Club"]["participants"]
```

## Troubleshooting

### Tests Fail Due to State Pollution

**Problem:** Tests pass individually but fail when run together.

**Solution:** Ensure `reset_activities` fixture is working. Check that it has `autouse=True`.

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:** Ensure `pythonpath = .` is set in `pytest.ini` and you're running pytest from the project root.

### Coverage Not Working

**Problem:** Coverage report shows 0% or missing files.

**Solution:** Ensure you're running from the project root and the `--cov=src` flag is set correctly.

## Continuous Integration

Example GitHub Actions workflow for running tests:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests with coverage
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest Markers](https://docs.pytest.org/en/stable/example/markers.html)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

## Contributing

When adding new features to the application:

1. Write tests first (TDD approach) or alongside implementation
2. Ensure all existing tests still pass
3. Maintain or improve code coverage (target: >90%)
4. Add integration tests for new endpoints
5. Add unit tests for new business logic
6. Update this README if adding new test patterns or fixtures
