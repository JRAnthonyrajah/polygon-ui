# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Polygon UI is a library/framework of UI components for Qt/PySide, similar to Mantine for web applications. This is a Python package built with Poetry for dependency management and uses a modern Python development stack.

## Development Commands

### Environment Setup
```bash
# Complete project setup (pyenv, virtualenv, poetry)
task setup

# Clean poetry virtualenv
task clean

# Open poetry shell
task shell
```

### Running the Application
```bash
# Run main entry point
task run
# or
poetry run polygon-ui

# Launch PolyBook component workshop
task polybook
# or
poetry run polybook
```

### Testing
```bash
# Run all tests
task test
# or
poetry run pytest

# Run tests in watch mode
task test-watch
# or
poetry run ptw --runner "pytest"

# Run tests with coverage
task coverage
# or
poetry run pytest --cov=src/polygon_ui --cov-report=html --cov-report=term

# Run single test file
poetry run pytest tests/test_basic.py
```

### Code Quality
```bash
# Run all linting checks
task lint

# Individual linters
task lint:ruff          # Ruff linter
task lint:mypy          # MyPy type checker
task lint:black-check   # Black formatting check

# Auto-fix linting issues
task fix
# or
poetry run ruff check --fix .
poetry run black .

# Format code
task format
# or
poetry run black .
```

### Versioning & Commits
```bash
# Conventional commits
cz commit

# Bump version and update changelog
cz bump

# Push with tags
git push && git push --tags
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## Architecture

### Project Structure
- `src/polygon_ui/` - Main package directory
  - `__init__.py` - Package initialization with version and hello function
  - `main.py` - Application entry point with logging configuration
  - `settings/config.toml` - Application configuration file
- `tests/` - Test directory with pytest configuration
- `Taskfile.yml` - Task runner configuration for common commands
- `.pre-commit-config.yaml` - Pre-commit hooks for code quality

### Package Configuration
- **Python Version**: 3.10+ (managed via pyenv)
- **Package Manager**: Poetry with `src/` layout
- **Entry Point**: `polygon_ui.main:main()`
- **Configuration**: TOML-based settings in `src/polygon_ui/settings/`

### Development Stack
- **Testing**: pytest with coverage support
- **Linting**: Ruff (linting), MyPy (type checking), Black (formatting)
- **Version Management**: Commitizen for conventional commits and semantic versioning
- **Task Runner**: Task (Taskfile.yml) for common development commands
- **Environment**: pyenv + Poetry virtual environments

### Key Patterns
- Uses `src/` layout for clean package structure
- Configuration stored in TOML files
- Logging configured in main entry point
- Tests discover source code via `pythonpath = src` in pytest.ini
- All development commands abstracted through Task tasks
- Pre-commit hooks enforce code quality automatically
- Poetry scripts provide CLI access (`polygon-ui` and `polybook`)

## Development Notes

- The project is currently in early development with basic hello functionality
- Intended to become a comprehensive Qt/PySide UI component library
- Uses conventional commit format enforced by Commitizen
- Version is synchronized between `pyproject.toml` and `src/polygon_ui/__init__.py`
- Supports HTML coverage reports generated in `htmlcov/` directory
