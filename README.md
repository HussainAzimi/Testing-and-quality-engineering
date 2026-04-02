# Run instructions 
## The test suit includes:
- **Unit tests** for domain logic and state transitions.
- **Parametrized tests** for multiple behavioral scenarios.
- **Interaction tests** using mocks for external services.
- **ventBus tests**  for handler ordering and failure isolation.
- **Integration tests** covering the full workfow.
- **Fixtures** for reusable and readable test setup.

The goal is to ensure confidence in bahavior rather than simply achieving high code coverage.

## Run tests
### To run all suite tests
``
pytest
``

### To run single test
``
pytest tests/test_order.py
pytest tests/test_event_bus.py
pytest tests/test_integration_workflow.py
pytest tests/conftest.py
``

### Run with coverage
``
pytest --cov=src
``
