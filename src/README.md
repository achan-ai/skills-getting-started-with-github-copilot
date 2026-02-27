# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Testing

The application includes a comprehensive test suite with unit and integration tests.

### Installation

Install dependencies including test packages:

```bash
pip install -r requirements.txt
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest tests/test_integration.py
pytest tests/test_unit.py
```

**Run tests by marker:**
```bash
pytest -m integration  # Run only integration tests
pytest -m unit         # Run only unit tests
```

### Code Coverage

**Run tests with coverage report:**
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

**View HTML coverage report:**
```bash
# The coverage report is generated in htmlcov/index.html
# Open it in your browser:
xdg-open htmlcov/index.html  # Linux
open htmlcov/index.html      # macOS
start htmlcov/index.html     # Windows
```

### Test Structure

```
tests/
├── __init__.py           # Package initialization
├── conftest.py           # Shared fixtures and configuration
├── test_integration.py   # Integration tests for API endpoints
├── test_unit.py          # Unit tests for data structures
└── README.md             # Testing documentation
```

### What's Tested

- ✅ **GET /activities** - List all activities with proper structure
- ✅ **POST /activities/{activity_name}/signup** - Sign up for activities
  - Success scenarios
  - Error cases (activity not found, already signed up, activity full)
  - URL encoding for activity names with spaces
- ✅ **DELETE /activities/{activity_name}/participants** - Unregister from activities
  - Success scenarios
  - Error cases (activity/participant not found)
- ✅ **State management** - Test isolation and data reset between tests
- ✅ **Data structure validation** - Activity schema and field types

### Test Fixtures

The test suite uses pytest fixtures for reusability:

- `client` - FastAPI TestClient instance
- `reset_activities` - Resets in-memory state after each test (auto-use)
- `sample_emails` - Test email addresses for signup/unregister operations
- `activity_names` - List of valid activity names
- `filled_activity` - Pre-filled activity at max capacity for testing

For more details, see [tests/README.md](../tests/README.md).
