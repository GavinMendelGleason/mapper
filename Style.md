# Moonshine Project Style Guide

This document outlines the coding standards and best practices for the Moonshine project.

## Code Formatting

### Black

- All Python code must be formatted using Black with default settings.
- Line length follows Black's default of 88 characters.

## Type Annotations

- All function signatures must include type annotations.
- Return types must be explicitly specified, including `-> None` when appropriate.
- Use the `typing` module for complex types (List, Dict, Optional, etc.).
- For Python 3.9+, use built-in generics (list, dict) instead of typing equivalents when possible.

Example:
```python
def process_data(input_data: list[str], max_items: int = 10) -> dict[str, int]:
    # Function implementation
    return result
```

## Data Validation with Pydantic

### Model Definitions

- Use Pydantic for all data models and configuration objects.
- Define clear field types and validation rules.
- Use descriptive field names and include field descriptions.

Example:
```python
from pydantic import BaseModel, Field

class Customer(BaseModel):
    id: int = Field(..., description="Unique customer identifier")
    name: str = Field(..., description="Customer's full name")
    active: bool = Field(True, description="Whether the customer is active")

    class Config:
        frozen = True  # Makes instances immutable
```

### Validation

- Validate all external data inputs using Pydantic models.
- Handle validation errors explicitly and provide clear error messages.
- Use Pydantic's built-in validation features (regex, min/max values, etc.) when appropriate.

## Documentation

- All modules, classes, and functions must have docstrings.
- Use Google-style docstrings format.
- Document parameters, return values, and exceptions.

Example:
```python
def calculate_total(prices: list[float], discount: float = 0.0) -> float:
    """
    Calculate the total price after applying a discount.

    Args:
        prices: List of item prices.
        discount: Discount rate as a decimal (0.1 = 10% discount).

    Returns:
        The total price after discount.

    Raises:
        ValueError: If discount is negative or greater than 1.
    """
    # Implementation
```

## Imports

- Organize imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Sort imports alphabetically within each group.
- Use absolute imports rather than relative imports.

## Error Handling

- Use specific exception types rather than catching generic exceptions.
- Always include meaningful error messages.
- Use context managers (`with` statements) for resource management.

## Testing

- Use pytest for testing
- Aim for high test coverage, especially for critical paths.
- Use descriptive test names that explain what is being tested.

## Variable Naming

- Use snake_case for variables, functions, and methods.
- Use PascalCase for classes and type variables.
- Use UPPER_CASE for constants.
- Choose descriptive names that reflect purpose rather than implementation.

## Function Design

- Functions should do one thing and do it well.
- Keep functions short and focused.
- Use default parameter values when appropriate.
- Return early to avoid deep nesting.

## Comments

- Write comments to explain "why" not "what".
- Keep comments up-to-date with code changes.
- Use TODO comments for planned improvements (format: `# TODO: description`).

## Version Control

- Write clear, concise commit messages.
- Each commit should represent a logical unit of change.
- Reference issue numbers in commit messages when applicable.

## Dependencies

- Explicitly declare all dependencies in pyproject.toml.
- Pin dependency versions to ensure reproducibility.
- Regularly update dependencies to address security vulnerabilities.
