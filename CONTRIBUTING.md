# Contributing to GeoVision AI Digital Twin

## Getting Started

1. **Fork and clone** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Make changes** and write tests
5. **Commit with clear messages**: `git commit -m "feat: description"`
6. **Push and create a Pull Request**

## Code Style

- **Python**: Follow PEP 8 (use `black` for formatting)
- **Docstrings**: Google-style docstrings for all functions/classes
- **Type Hints**: Use type annotations for function signatures
- **Comments**: Use docstrings, not inline comments unless necessary

## Testing

- Write unit tests for all new functionality
- Run tests: `pytest tests/`
- Aim for >80% code coverage
- Use fixtures for reusable test components

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:
```
feat: Add fire spread animation export

Implements VTK export for fire spread history to enable
ParaView visualization. Includes time-series burn progression.

Closes #42
```

## Pull Request Process

1. **Title**: Clear, concise description
2. **Description**: What changed and why
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update relevant docs
5. **Reviewers**: Request review from maintainers
6. **CI/CD**: Ensure all checks pass

## Module Development Guidelines

### Creating a New Simulation Module

1. Create module directory: `ai_models/your_module/`
2. Include standard files:
   - `__init__.py` - Package initialization
   - `README.md` - Module documentation
   - `model.py` - Core simulation logic
   - `tests.py` - Unit tests
3. Export main class in `__init__.py`
4. Add to main documentation

### Creating a Data Loader

1. Create in `data_pipeline/loaders/`
2. Inherit from `BaseLoader` interface
3. Implement methods:
   - `load(path)` - Load data
   - `validate()` - Validate format
   - `to_array()` - Convert to numpy
4. Add error handling and logging

## Documentation

- Update relevant `.md` files
- Add docstrings to code
- Include usage examples
- Document parameters and return values

## Reporting Issues

- **Bug**: Use bug template, include reproducible steps
- **Feature**: Use feature template, explain use case
- **Question**: Use discussion, not issues

## Contact

- Create an issue for technical questions
- Tag maintainers for urgent matters
