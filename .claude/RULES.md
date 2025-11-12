# Coding Rules

This file provides coding standards and guardrails for AI assistants and developers working on this project.

## General Python Standards

- Follow PEP 8 style guidelines (enforced by Black formatter)
- Use type hints for function parameters and return values
- Add docstrings for all public functions, classes, and modules
- Keep functions focused and small (prefer composition over long scripts)
- Use meaningful variable and function names that express intent

## Code Quality

- Do not modify file formatting style manually - Black handles this
- Use structured logging instead of print statements
- Include error context in log messages
- Handle exceptions appropriately - catch specific exceptions, not bare except
- Prefer explicit error handling over silent failures

## Dependencies and Imports

- Add new dependencies via `poetry add <package>` or `poetry add --group dev <package>`
- Keep imports organized: stdlib, third-party, local (Black will enforce this)
- Avoid circular imports by restructuring code when they occur

## Testing

- Write tests for new functionality using pytest
- Place tests in the `tests/` directory mirroring the source structure
- Use fixtures for setup/teardown, not manual state management
- Use mocks/fakes for external dependencies - do not call real services in tests
- Test file names must start with `test_` to be discovered by pytest

## Security and Secrets

- Never include secrets, API keys, or credentials in code
- Use environment variables or `.env` files (which are gitignored) for secrets
- Use placeholder values like `<API_KEY>` or `your-api-key-here` in examples
- Review `.gitignore` before committing to ensure sensitive files are excluded

## Version Control

- Use Commitizen for commits: `cz commit` for interactive commit creation
- Follow conventional commit format: `type(scope): description`
  - Types: feat, fix, docs, style, refactor, test, chore
- Keep commits atomic and focused on a single change
- Do not commit directly to main/master - use feature branches

## Configuration

- Store configuration in `src/polygon_ui/settings/`
- Use environment variables for deployment-specific config
- Provide sensible defaults where possible
- Document all configuration options

## Error Handling

- Use custom exceptions for domain-specific errors
- Log errors with sufficient context for debugging
- Provide user-friendly error messages at API/UI boundaries
- Handle timeouts and retries for external service calls

## Documentation

- Keep README.md updated with setup and usage instructions
- Document complex algorithms or business logic inline
- Update CHANGELOG.md via `cz bump` (automatic)
- Prefer code clarity over excessive comments
