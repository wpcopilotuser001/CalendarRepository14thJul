---
name: unit-script-generator
description: "Use this skill when the user asks to generate unit scripts, unit tests, test files, test stubs, or coverage-focused tests for existing or new code. Handles Python pytest, JavaScript/TypeScript (Jest/Vitest), and framework-specific test conventions when present in the repository."
---

# Unit Script Generator

## Purpose

Generate focused, runnable unit test scripts aligned with the current repository conventions.

## When To Use

Use this skill when the user asks to:
- create unit scripts
- add unit tests
- improve unit test coverage
- generate test files for a function, class, component, hook, or service

Do not use this skill for:
- end-to-end tests
- load or performance testing
- broad integration test plans without code changes

## Inputs To Collect From The User

If missing, ask for:
- target file(s) or symbol(s)
- desired test framework if multiple are available
- scope (happy path only or include edge/error paths)

## Workflow

1. Discover project test stack:
- Inspect dependency files and existing test folders.
- Prefer existing conventions over introducing new frameworks.

2. Identify target behaviors:
- Read implementation code.
- Enumerate expected outcomes, edge cases, and failure modes.

3. Create or update tests:
- Add tests near existing tests following local naming rules.
- Keep tests deterministic and isolated.
- Use descriptive behavior-driven test names.

4. Run and verify:
- Execute the relevant test command for the changed area.
- If tests fail, fix only issues related to the requested scope unless user asks for broader fixes.

5. Report results:
- Summarize files changed.
- State command run and outcome.
- Mention any untested risks.

## Test Design Rules

- Follow Arrange / Act / Assert structure.
- One behavior per test.
- Mock external I/O (network, filesystem, time) where feasible.
- Avoid brittle timing assertions.
- Use fixtures/factories for repeated setup.
- Include at least:
  - success path
  - input validation or edge path
  - error path (where applicable)

## Language Conventions

### Python (pytest)

- Prefer pytest style with plain assert statements.
- File naming: test_<module>.py.
- Use monkeypatch or unittest.mock for isolation.

Example layout:

```python
# Arrange
value = 10

# Act
result = fn_under_test(value)

# Assert
assert result == 20
```

### JavaScript/TypeScript (Jest or Vitest)

- Use existing framework found in repository.
- Prefer describe/it blocks with clear behavior names.
- Mock external modules and timers as needed.

Example layout:

```ts
describe('sum', () => {
  it('returns total for valid numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });
});
```

## Command Guidance

Use existing project commands first. Typical fallbacks:
- Python: pytest -q
- Node: npm test
- Vitest: npx vitest run

Do not add new tooling unless user requests it.

## Output Contract

After generating tests, provide:
- list of changed test files
- what behaviors are covered
- exact command executed
- pass/fail summary
- follow-up suggestions only if meaningful gaps remain
