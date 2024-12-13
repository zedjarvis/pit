#!/usr/bin/env python3
"""
This script initializes a simple distributed source control repository.

The repository structure:
- `.pit/objects`: Stores objects like blobs and trees.
- `.pit/refs/heads`: Stores branch references.
- `.pit/HEAD`: Tracks the current branch.
- `.pit/index`: Serves as a staging area.
- `.pit/config`: Contains user configuration.

Usage:
Run this script to create a `.pit` directory in the current working directory.

"""

import os

from src.constants import MAIN_BRANCH, PIT_DIR
from src.utils import write_file


def init_repo(args):
    """
    Initializes a new pit repository in the current directory.

    Creates a `.pit` directory with the following structure:
    - objects: Directory to store repository objects.
    - refs/heads: Directory to store branch references.
    - HEAD: File to store the current branch pointer.
    - index: File to act as a staging area.
    - config: File for user configuration.

    Args:
        args: Any additional arguments passed to the script (unused in this function).

    Prints:
        A message indicating whether the repository was initialized successfully
        or already exists.
    """
    if os.path.exists(PIT_DIR):
        print("Repository already initialized.")
        return

    os.makedirs(f"{PIT_DIR}/objects")
    os.makedirs(f"{PIT_DIR}/refs/heads")
    write_file(f"{PIT_DIR}/HEAD", f"ref: refs/heads/{MAIN_BRANCH}\n")
    write_file(f"{PIT_DIR}/index", "")
    write_file(f"{PIT_DIR}/config", "[user]\n\tname = Your Name\n\temail = email@example.com\n")

    print(f"Initialized empty repository in {PIT_DIR}/")