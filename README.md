# pre-commit-hooks

Different pre-commit hooks.

For usage see: https://github.com/pre-commit/pre-commit

## Hooks available

`branch-name-validator-hook`

Allow commits only on branches with certain names or patterns. Branch names and patterns may be specified multiple times.

This example allows commits to the branch named _test_ and to branches whose names start either with _feature\_ticket\_number_ followed by some digits or that start with _fix_ followed by any characters:

```
repos:
-   repo: https://github.com/FabianSchlueter/pre-commit-hooks
    rev: v1.0.0 # Use the ref you want to point at
    hooks:
    -   id: branch-name-validator-hook
        args:
          - -b
          - test
          - -p
          - ^feature_ticket_number\d*$
          - -p
          - ^fix.*$
        pass_filenames: false
```

`python-docstring-checker`

Check for docstrings in custom Python function definitions.

This example checks in all Python files whose name contains the string _test_ if there are any function definitions with a missing docstring. For checking all Python files leave out the _files_ operator

```
repos:
-   repo: https://github.com/FabianSchlueter/pre-commit-hooks
    rev: v1.2.0 # Use the ref you want to point at
    hooks:
    -   id: docstring-checker
        files: test
```