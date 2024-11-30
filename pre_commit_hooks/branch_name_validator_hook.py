import re
import subprocess
import sys
from typing import Sequence, Optional
import argparse
import logging

logging.basicConfig(level=logging.INFO)

def get_current_branch():
    """Gets the name of the current Git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        logging.info(f"Error getting current branch: {e.stderr.decode()}")
        sys.exit(1)


def main(argv: Optional[Sequence[str]] = None):

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--branch', action='append',
        help='branch to allow commits to, may be specified multiple times',
    )
    parser.add_argument(
        '-p', '--pattern', action='append',
        help=(
            'regex pattern for branch name to allow commits to, '
            'may be specified multiple times'
        ),
    )
    args = parser.parse_args(argv)

    current_branch = get_current_branch()

    if args.branch and not args.pattern:
        if current_branch in frozenset(args.branch):
            logging.info(f"Branch Name Validator Hook Success: Commits are allowed to the current branch '{current_branch}'.")
            sys.exit(0)
        else:
            logging.info(f"Branch Name Validator Hook Error: Commits not allowed to this branch. Branch name must be one of the following: {args.branch}.")
            sys.exit(1)
    elif not args.branch and args.pattern:
        for p in frozenset(args.pattern):
            if re.match(p, current_branch):
                    logging.info(f"Branch Name Validator Hook Success: Commits allowed to the current branch. Branch name '{current_branch}' matches the pattern '{p}'.")
                    sys.exit(0)
        logging.info(f"Branch Name Validator Hook Error: Commits not allowed to this branch. Branch name must match any of the patterns '{args.pattern}'.")
        sys.exit(1)
    elif args.branch and args.pattern:
        if current_branch in frozenset(args.branch) or any(re.match(p, current_branch) for p in frozenset(args.pattern)):
            logging.info(f"Branch Name Validator Hook Success: Commits allowed to the current branch. Commits are allowed to the current branch '{current_branch}' or it matches one of the patterns '{args.pattern}'.")
            sys.exit(0)
        else:
            logging.info(f"Branch Name Validator Hook Error: Commits not allowed to this branch. Branch name must be one of the following: {args.branch}. Or it must match any of the patterns '{args.pattern}.")
            sys.exit(1)


if __name__ == "__main__":
    main()
