import os
import ast
from collections import defaultdict


def find_python_files(path):

    files = []

    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(".py"):
                files.append(os.path.join(root, f))

    return files


def is_test_file(file):

    name = os.path.basename(file).lower()

    return (
        name.startswith("test")
        or name.endswith("_test.py")
        or "/tests/" in file.replace("\\", "/")
    )


def detect_private_access(content):

    return "._" in content


def detect_mock_usage(content):

    keywords = [
        "patch(",
        "MagicMock(",
        "Mock("
    ]

    return any(k in content for k in keywords)


def extract_imports(file):

    with open(file, "r", encoding="utf8") as f:
        try:
            tree = ast.parse(f.read())
        except Exception:
            return []

    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for name in node.names:
                imports.append(name.name)

        if isinstance(node, ast.ImportFrom):

            if node.module:
                imports.append(node.module)

    return imports


def analyze_tests(repo_path):

    files = find_python_files(repo_path)

    test_files = [f for f in files if is_test_file(f)]

    signals = []

    private_access_count = 0
    mock_usage_count = 0

    dependency_map = defaultdict(list)

    for file in test_files:

        with open(file, "r", encoding="utf8") as f:
            content = f.read()

        if detect_private_access(content):
            private_access_count += 1

        if detect_mock_usage(content):
            mock_usage_count += 1

        imports = extract_imports(file)

        for imp in imports:
            dependency_map[imp].append(file)

    if private_access_count > 0:

        signals.append({
            "signal": "implementation_coupling",
            "severity": "medium",
            "count": private_access_count
        })

    if mock_usage_count > 10:

        signals.append({
            "signal": "mock_dependency_instability",
            "severity": "medium",
            "count": mock_usage_count
        })

    cascade_risk = []

    for module, tests in dependency_map.items():

        if len(tests) > 8:

            cascade_risk.append({
                "module": module,
                "tests": len(tests)
            })

    if cascade_risk:

        signals.append({
            "signal": "cascade_fragility",
            "severity": "high",
            "modules": cascade_risk
        })

    return signals, len(test_files)


def run(repo_path):

    signals, test_count = analyze_tests(repo_path)

    print("\nTest Suite Structural Audit\n")

    print(f"Test files analyzed: {test_count}\n")

    if not signals:
        print("No structural signals detected.\n")
        return

    print("Signals detected:\n")

    for s in signals:
        print(s)


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:
        print("Usage: python test_audit.py <repo_path>")
        sys.exit(1)

    run(sys.argv[1])
