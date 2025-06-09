# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
make install                    # Install virtual environment and pre-commit hooks
```

### Code Quality and Testing
```bash
make check                      # Run all code quality tools (pre-commit, mypy, deptry)
make test                       # Run tests with coverage
uv run pre-commit run -a        # Run pre-commit hooks on all files
uv run mypy                     # Type checking
uv run pytest                  # Run tests
uv run pytest path/to/test.py   # Run specific test file
```

### Build and Documentation
```bash
make build                      # Build wheel package
make docs                       # Serve documentation locally
make docs-test                  # Test documentation build
```

## Project Architecture

This is an Amazon Pay Per Click (PPC) MCP server built with Python and uv for dependency management. The project follows a standard Python package structure:

- **Source code**: Located in `src/amazon_ppc_mcp_server/`
- **Tests**: Located in `tests/` with pytest
- **Documentation**: MkDocs with Material theme, auto-generated from docstrings
- **Package management**: Uses uv instead of pip/poetry
- **Code quality**: Enforced via ruff (linting/formatting), mypy (type checking), pre-commit hooks

The project is currently in early development with placeholder code in `foo.py`. The main package structure expects Amazon PPC server functionality to be implemented within the `amazon_ppc_mcp_server` module.

## Key Configuration

- **Python versions**: 3.9-3.13 supported
- **Testing**: pytest with coverage reporting
- **Linting**: ruff with comprehensive rule set (line length: 120)
- **Type checking**: mypy with strict settings
- **Pre-commit**: Automatically runs code quality checks
- **CI/CD**: GitHub Actions with tox for multi-version testing

## Development Best Practices

- When accessing GitHub, preferentially use the 'gh' command in bash