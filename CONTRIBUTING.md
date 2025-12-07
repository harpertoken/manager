# Contributing to Manager

Thank you for your interest in contributing to Manager! This document provides guidelines for development.

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -e .[test]`
3. Install pre-commit hooks: `pre-commit install`

## Code Quality

We use the following tools for code quality:

- **Linting**: `ruff check .`
- **Formatting**: `ruff format .`
- **Full checks**: `pre-commit run --all-files`
- **Tests**: `pytest`
- **Build**: `python -m build`

## Commit Messages

Follow conventional commits:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `chore:` for maintenance
- `test:` for tests

Messages must be lowercase, ≤40 characters first line.

## Pull Requests

- Ensure all checks pass
- Update documentation if needed
- Add tests for new features
