# Backend Tests

This directory contains backend FastAPI tests for the `src/app.py` application.

## Running tests

Install the dependencies from `requirements.txt` and run:

```bash
pytest -q
```

## Test style

The tests use the Arrange-Act-Assert (AAA) pattern for clarity:

- Arrange: create the `TestClient`, test inputs, and expected results
- Act: send the request to the API endpoint
- Assert: verify the response status, body, and any side effects

## Files

- `tests/test_app.py` — API route tests for `/`, `/activities`, signup, and unregister flows
