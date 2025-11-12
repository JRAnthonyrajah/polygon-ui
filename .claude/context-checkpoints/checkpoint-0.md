# Context: Polygon UI - PolyBook UI Improvements

**Project**: polygon-ui
**Branch**: master
**Goal**: Fix PolyBook visibility and layout issues
**Status**: Starting workflow
**Timestamp**: 2025-11-12 18:59

## Problem Statement
PolyBook has visibility and layout issues:
- Text is not clearly visible
- Components are jumbled up and poorly organized
- UI needs better spacing, contrast, and organization

## Current State
- PolyBook is a Qt/PySide GUI application for component development
- Has component registry, stories, props editor, and preview functionality
- Current implementation has UI/UX problems affecting usability

## Target State
- Clear, readable text with proper contrast
- Well-organized component layout
- Professional-looking interface
- Improved user experience for component development

## Success Criteria
- All text is clearly visible with proper contrast
- Components are properly organized and spaced
- Interface is professional and user-friendly
- All existing functionality is preserved

---

## Project Overview

**Project:** Polygon UI
**Description:** A library/framework of UI components for Qt/PySide, similar to Mantine for webapps

## Project Structure

```
polygon-ui/
├── src/polygon_ui/    # Main package source code
│   ├── __init__.py                         # Package initialization, version info
│   └── settings/                           # Configuration files
│       ├── .env                            # Environment variables (gitignored)
│       └── config.toml                     # Application configuration
├── tests/                                  # Test suite (pytest)
│   ├── __init__.py
│   └── test_basic.py                       # Sample tests
├── pyproject.toml                          # Poetry dependencies and project metadata
├── Taskfile.yml                            # Task runner commands
├── .pre-commit-config.yaml                 # Pre-commit hooks configuration
└── pytest.ini                              # Pytest configuration
```

## Technology Stack

- **Language:** Python 3.11
- **Package Manager:** Poetry
- **Task Runner:** Task (Taskfile)
- **Environment Manager:** pyenv + pyenv-virtualenv
- **Testing:** pytest, pytest-asyncio
- **Version Control:** Git with Commitizen for semantic versioning
- **Code Quality:** Black (formatter), pre-commit hooks

## Development Workflow

### Initial Setup

```bash
task setup        # Install Python version, create virtualenv, install dependencies
```

This command handles:
1. Installing Python 3.11 via pyenv
2. Creating isolated virtual environment
3. Installing Poetry dependencies

### Common Commands

```bash
task run                    # Run the application
task shell                  # Activate Poetry shell
poetry run pytest           # Run all tests
poetry run pytest tests/test_basic.py  # Run specific test file
pre-commit run --all-files  # Run code quality checks
```

### Adding Dependencies

```bash
poetry add <package>              # Add runtime dependency
poetry add --group dev <package>  # Add development dependency
poetry install                    # Install dependencies from lock file
```

### Version Management

This project uses **Commitizen** for automated semantic versioning:

- Commits must follow conventional commit format
- Version is tracked in `pyproject.toml` and `src/polygon_ui/__init__.py`
- Changelog is automatically generated and updated

```bash
cz commit                   # Interactive conventional commit
cz bump                     # Bump version based on commits, update CHANGELOG
git push && git push --tags # Push changes and version tags
```

## Code Organization Principles

- **Source code** lives in `src/polygon_ui/`
- **Tests** mirror source structure in `tests/`
- **Configuration** files in `src/polygon_ui/settings/`
- **Entry point** for application in `src/polygon_ui/main.py` (if created)

## Pre-commit Hooks

Automatically enforced on every commit:
- **Black:** Code formatting
- **Trailing whitespace removal**
- **End-of-file fixer**
- **YAML validation**
- **Commitizen:** Conventional commit message validation

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push/PR:
- Install dependencies
- Run test suite
- Ensures tests pass before merging

## Configuration Management

- Environment-specific config: Use `.env` file (never commit this)
- Application config: Use `config.toml` (can be committed)
- Access config in code through environment variables or config loaders

## Error Handling Strategy

- Use structured logging for all output
- Catch specific exceptions rather than broad try/except blocks
- Log errors with sufficient context for debugging
- Provide clear error messages to users

## Testing Philosophy

- Write tests for new functionality
- Use fixtures for test setup
- Mock external dependencies (APIs, databases, etc.)
- Keep tests fast and isolated
- Run tests before committing: `poetry run pytest`
