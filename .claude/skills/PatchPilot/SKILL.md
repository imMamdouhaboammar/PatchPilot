```markdown
# PatchPilot Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the PatchPilot Python codebase. You'll learn how to structure files, write and organize code, follow commit message conventions, and understand the project's approach to testing. These guidelines ensure consistency and maintainability across the project.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - **Example:** `data_processor.py`, `user_service.py`

### Import Style
- Use **relative imports** within the codebase.
  - **Example:**
    ```python
    from .utils import parse_config
    ```

### Export Style
- Use **named exports** (explicitly define what is exported).
  - **Example:**
    ```python
    def process_data(data):
        # ...implementation...
        return result

    __all__ = ['process_data']
    ```

### Commit Messages
- Follow **conventional commit** patterns.
- Use the `feat` prefix for new features.
- Keep commit messages concise (average 61 characters).
  - **Example:**
    ```
    feat: add user authentication to login endpoint
    ```

## Workflows

### Feature Development
**Trigger:** When adding a new feature to the codebase  
**Command:** `/feature-development`

1. Create a new branch for your feature.
2. Implement the feature following coding conventions.
3. Write or update relevant tests.
4. Commit changes with a `feat:` prefix and a concise message.
5. Push your branch and open a pull request.

### Testing Code
**Trigger:** When verifying code correctness or before submitting changes  
**Command:** `/run-tests`

1. Identify test files (pattern: `*.test.*`).
2. Run all test files using the project's preferred test runner.
3. Review test results and fix any failures.
4. Repeat until all tests pass.

## Testing Patterns

- Test files follow the pattern: `*.test.*` (e.g., `user_service.test.py`).
- The specific testing framework is not defined; use standard Python testing tools (e.g., `pytest` or `unittest`).
- Place test files alongside the code or in a dedicated test directory.
- Write tests for all new features and bug fixes.

  **Example test file:**
  ```python
  # user_service.test.py
  from .user_service import process_user

  def test_process_user_valid():
      assert process_user("Alice") == "Processed: Alice"
  ```

## Commands
| Command              | Purpose                                      |
|----------------------|----------------------------------------------|
| /feature-development | Start a new feature development workflow     |
| /run-tests           | Run all tests in the codebase                |
```