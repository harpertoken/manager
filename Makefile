.PHONY: test lint format clean install dev-install

# Run tests with coverage
test:
	pytest --cov=manager --cov-report=term-missing

# Run linting
lint:
	ruff check .

# Format code
format:
	ruff format .

# Clean up
clean:
	rm -rf __pycache__ *.pyc .pytest_cache .coverage

# Install in editable mode
install:
	pip install -e .

# Install with dev dependencies
dev-install:
	pip install -e ".[test]"

# Run all checks
check: lint test
