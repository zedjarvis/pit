#!/usr/bin/env python3
"""
Pit Distributed Source Control System CLI

This script serves as the command-line interface (CLI) for the Pit Distributed Source Control System (DSCS).
It uses the argparse library to parse commands and arguments, allowing the user to perform various 
repository-related operations like initializing a repository, adding files, committing changes, 
viewing logs, branching, checking out branches, merging, and diffing.

Commands:
- init: Initialize a new repository
- add: Add files to the staging area
- commit: Commit staged changes
- log: View commit logs
- branch: Create and manage branches
- checkout: Switch branches or restore working tree files
- merge: Merge branches
- diff: Show differences between commits or working tree files
- clone: Clone a repository
"""

import argparse

from src import cli


def main():
    """
    Main entry point of the Distributed Source Control System CLI.

    This function sets up the argument parser, adds subcommands for each repository operation,
    and calls the appropriate function based on the user's input. The available commands are
    initialized by adding them to the subparsers through the `cli` module.

    Commands include: init, add, commit, log, branch, checkout, merge, and diff.

    Expects the user to provide one of the valid subcommands to interact with the system.
    """
    parser = argparse.ArgumentParser(description="Pit: Like Git but Awesome.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cli.add_init_command(subparsers)
    cli.add_add_command(subparsers)
    cli.add_status_command(subparsers)
    cli.add_commit_command(subparsers)
    cli.add_log_command(subparsers)
    cli.add_branch_command(subparsers)
    cli.add_checkout_command(subparsers)
    cli.add_merge_command(subparsers)
    cli.add_diff_command(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
