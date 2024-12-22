import ast
import sys
import argparse
from typing import Optional, Sequence


class DocstringChecker(ast.NodeVisitor):
    def __init__(self, file_path):
        self.errors = []
        self.file_path = file_path

    def visit_FunctionDef(self, node):
        if not ast.get_docstring(node):
            self.errors.append(f"Function '{node.name}' on line {node.lineno} in file '{self.file_path}' is missing a docstring.")
        self.generic_visit(node)

def check_docstrings(file_path: str) -> bool:
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
    checker = DocstringChecker(file_path)
    checker.visit(tree)
    if checker.errors:
        for error in checker.errors:
            print(error)
        return False
    return True

def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='Files to check for docstrings')
    args = parser.parse_args(argv)

    all_passed = True
    for file_path in args.files:
        if file_path.endswith('.py'):
            if not check_docstrings(file_path):
                all_passed = False

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()