#!/usr/bin/env python3
"""
This is the main cli entry point for parsing the args and running the related functions
"""

from src import branch, commit, diff, merge, repository, staging, status


def add_init_command(subparsers):
    """
    this function adds a subcommand 'init' to the provided subparsers, which, when executed,
    will call the `init_repo` function to initialize a new repository.
    """
    parser = subparsers.add_parser("init", help="Initialize a new repository")
    parser.set_defaults(func=repository.init_repo)


def add_add_command(subparsers):
    """
    this function adds a subcommand 'add' to the provided subparsers, which, when executed,
    will call the `add_files` function to add files to staging.
    """
    parser = subparsers.add_parser("add", help="Stage files for commit")
    parser.add_argument("files", nargs="+", help="Files to stage")
    parser.set_defaults(func=staging.add_files)


def add_status_command(subparsers):
    """ """
    parser = subparsers.add_parser(
        "status", help="Show the current status of the repository"
    )
    parser.set_defaults(func=status.status)


def add_commit_command(subparsers):
    parser = subparsers.add_parser("commit", help="Commit staged changes")
    parser.add_argument("-m", "--message", required=True, help="Commit message")
    parser.set_defaults(func=commit.commit_changes)


def add_log_command(subparsers):
    parser = subparsers.add_parser("log", help="View commit history")
    parser.set_defaults(func=commit.view_log)


def add_branch_command(subparsers):
    parser = subparsers.add_parser("branch", help="Create a new branch")
    parser.add_argument("branch_name", help="Name of the new branch")
    parser.set_defaults(func=branch.create_branch)


def add_checkout_command(subparsers):
    parser = subparsers.add_parser("checkout", help="Switch to a branch")
    parser.add_argument("branch_name", help="Name of the branch to switch to")
    parser.set_defaults(func=branch.checkout_branch)

def add_merge_command(subparsers):
    parser = subparsers.add_parser("merge", help="Merge another branch into current branch")
    parser.add_argument("branch_name", help="Branch to merge")
    parser.set_defaults(func=merge.merge_branch)

def add_diff_command(subparsers):
    parser = subparsers.add_parser("diff", help="Show differences between commits and working directory")
    parser.set_defaults(func=diff.show_diff)