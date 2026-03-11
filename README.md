
# test-audit

**Detect brittle tests and implementation-coupled test suites.**

`test-audit` analyzes a repository’s test suite and identifies structural patterns that often lead to fragile tests.

Instead of asking:

* Do the tests pass?

This tool asks:

* Are the tests verifying **behavior** or **implementation details**?
* Will a refactor break large portions of the test suite?
* Are tests overly dependent on mocks or private internals?

The goal is to help developers build **tests that verify behavior**, not just detect code changes.

---

# Why This Exists

Modern tooling makes it very easy to generate tests automatically. AI tools, in particular, often produce tests that look correct but are tightly coupled to implementation details.

Example:

```python
assert graph._adjacency["A"] == ["B"]
```

This test verifies a **private data structure**, not the behavior of the system. If the internal implementation changes, the test breaks even though the system still works.

This tool helps detect those patterns early.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_ORG/structural-scan.git
cd structural-scan
```

Python 3.9+ required.

No additional dependencies.

---

# Usage

Run the audit against a repository:

```bash
python test_audit.py /path/to/repository
```

Example:

```bash
python test_audit.py .
```

---

# Example Output

```
Test Suite Structural Audit

Test files analyzed: 27

Signals detected:

implementation_coupling
  tests referencing private attributes: 9

mock_dependency_instability
  excessive mocking detected: 14

cascade_fragility
  module: graph_core
  tests dependent: 11
```

---

# Signals Explained

### Implementation Coupling

Tests access internal implementation details such as:

* private attributes (`._something`)
* internal data structures
* algorithm steps

These tests often fail during refactoring even when system behavior remains correct.

---

### Mock Dependency Instability

Large numbers of mocks may indicate tests verifying **wiring rather than behavior**.

Over-mocking can make tests brittle and reduce their ability to detect real regressions.

---

### Cascade Fragility

Many tests depend on the same internal module.

This creates a **cascade risk**, where a small change in that module causes widespread test failures.

---

# Philosophy

Good tests verify **observable behavior**.

They should remain valid even if:

* internal data structures change
* algorithms are rewritten
* implementation details evolve

If refactoring breaks large parts of the test suite, the tests may be acting as **change detectors**, not behavioral verification.

---

# What This Tool Is

* a lightweight structural analysis tool
* a quick diagnostic for test suite health
* an experiment in structural observability for software systems

---

# What This Tool Is Not

* a test framework
* a linter
* a static analyzer
* a replacement for human review

It complements existing tools by examining **how tests relate structurally to the codebase**.

---

# When to Use It

Developers may run `test-audit` when:

* introducing AI-generated tests
* preparing for a major refactor
* evaluating the health of a legacy test suite
* reviewing test architecture in a large repository

---

# Roadmap

Future improvements may include:

* deeper AST analysis of test assertions
* detection of behavioral invariant tests
* visualization of test dependency cascades
* integration with CI pipelines

---

# License

MIT License.

---

# Contributing

Contributions are welcome.

Areas that would be especially valuable:

* better detection of behavioral vs structural assertions
* language support beyond Python
* improved mock analysis
* richer reporting

---

# A Note

The idea behind `test-audit` is simple:

**Tests are part of the system architecture.**

Like any architecture, they can become structurally fragile.

This tool explores ways to make that fragility visible.

---

If you'd like, I can also draft the **top-level repository README** that ties all three tools together (`structural-scan`, `test-audit`, `cascade-map`) so the project reads like a coherent new category rather than three random scripts.
