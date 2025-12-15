# Pre-Push Review Command

Review all staged and unstaged changes against fmpsdk SDK coding standards.

**Goal:** Ensure consistency and quality in the fmpsdk Python SDK before committing.

## Process

### Step 1: Identify Changed Files

Run these commands to get all changed files:

```bash
# Get all changed files (staged and unstaged)
git diff --name-only HEAD
git diff --cached --name-only
```

### Step 2: Categorize Changes

Focus on Python files in `fmpsdk/` directory:
- **SDK modules:** `fmpsdk/*.py`
- **Root files:** `*.py` (example files, MCP server)
- **Config:** `pyproject.toml`

### Step 3: Run Automated Checks

**Linting (if available):**
```bash
poetry run black --check fmpsdk/
poetry run isort --check fmpsdk/
poetry run flake8 fmpsdk/
```

**Type checking (if available):**
```bash
poetry run mypy fmpsdk/
```

Note: These may not be configured yet - skip if not available.

### Step 4: Verify __init__.py Consistency

For any new functions added to modules:

1. Check if function is imported in `fmpsdk/__init__.py`
2. Check if function is listed in `__all__`

```bash
# List all public functions (def without leading underscore)
grep "^def [^_]" fmpsdk/*.py

# Check __all__ list
grep -A 200 "^__all__" fmpsdk/__init__.py
```

### Step 5: Run Code Review Agent

For each changed `.py` file in `fmpsdk/`:

1. Read the file content
2. Get the diff: `git diff HEAD -- <filepath>`
3. Apply all BLOCK and WARN checks from `.claude/agents/code-reviewer.md`
4. Collect all issues

### Step 6: Generate Summary

Output format:

```markdown
## Pre-Push Review: [READY | BLOCKED]

### Automated Checks
- Black format: [PASS | FAIL | SKIPPED]
- Isort imports: [PASS | FAIL | SKIPPED]
- Flake8 lint: [PASS | FAIL | SKIPPED]
- Mypy types: [PASS | FAIL | SKIPPED]

### Export Consistency
- New functions exported: [YES | NO | N/A]
- __all__ list updated: [YES | NO | N/A]

### Code Review
- Files reviewed: X
- BLOCK issues: Y
- WARN issues: Z

### BLOCK Issues (must fix)
[List each with file:line and fix]

### WARN Issues (consider fixing)
[List each with file:line and explanation]

### Files Reviewed
- fmpsdk/module.py [status]

### Recommendation
[READY TO PUSH] or [FIX REQUIRED: list blocking issues]
```

## Arguments

- `$ARGUMENTS` (optional): Specific file or directory to review
  - If omitted, review all uncommitted changes
  - Can be a file path: `fmpsdk/financial_statements.py`
  - Can be a directory: `fmpsdk/`

## Usage Examples

```bash
# Review all uncommitted changes
/review-staged

# Review specific file
/review-staged fmpsdk/financial_statements.py

# Review all SDK modules
/review-staged fmpsdk/
```

## Quick Reference: What Gets Checked

### Python BLOCK Checks
1. Missing API_KEY usage from environment
2. Wrong API version (v3 vs v4) for endpoint
3. Missing format_output call for output parameter
4. New function not exported in __init__.py
5. Inconsistent function signature pattern
6. Missing type hints on public functions
7. File writes without context manager

### Python WARN Checks
1. Missing docstring
2. Missing :example: in docstring
3. Hardcoded limit instead of DEFAULT_LIMIT
4. Missing period validation
5. Broad exception handling
6. Missing error logging
