#!/usr/bin/env python3
"""
This script checks for the status of the files in the repository
"""
from src.utils import (get_modified_files, get_repo_dir, get_staged_files,
                       get_untracked_files)


def status(args):
    """
    Display the current status of the repository, showing staged, modified, and untracked files.

    Args:
        args: Command-line arguments (not used here, but required for CLI framework).
    """
    repo_dir = get_repo_dir()

    if not repo_dir:
        print("Error: Not a Pit repository (or any of the parent directories.)")
        return

    # Get staged, modified, and untracked files
    staged_files = get_staged_files(repo_dir)
    modified_files = get_modified_files(repo_dir)
    untracked_files = get_untracked_files(repo_dir)

    # Print status
    print("Repo status:")

    if staged_files:
        print("\nStaged for commit:")
        for file in staged_files:
            print(f" {file}")
    else:
        print("\nNo files staged for commit.")

    if modified_files:
        print("\nModified but not staged:")
        for file in modified_files:
            print(f"  {file}")
    else:
        print("\nNo modified files.")

    if untracked_files:
        print("\nUntracked files:")
        for file in untracked_files:
            print(f"  {file}")
    else:
        print("\nNo untracked files.")

    # If everything is clean
    if not staged_files and not modified_files and not untracked_files:
        print("\nYour working directory is clean.")
