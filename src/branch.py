#!/usr/bin/env python3

import os

from src.constants import PIT_DIR
from src.utils import ensure_repo, get_current_branch, read_file, write_file


def create_branch(args):
    # Ensure repo exists
    ensure_repo()

    branch_path = f"{PIT_DIR}/refs/heads/{args.branch_name}"
    if os.path.exists(branch_path):
        print(f"Branch {args.branch_name} already exists.")
        return

    # Get current branch
    current_branch = get_current_branch()

    # Get current commit
    current_commit = read_file(f"{PIT_DIR}/refs/heads/{current_branch}").strip()

    # Write current commit to new branch head
    write_file(branch_path, current_commit)

    print(f"Branch {args.branch_name} created.")


def checkout_branch(args):
    # Ensure repo exists
    ensure_repo()

    # Ensure no staged files
    staged_data = read_file(f"{PIT_DIR}/index")
    if staged_data:
        print("There is staged data commit first before switching.")
        return

    branch_path = f".pit/refs/heads/{args.branch_name}"
    # Make sure branch exists before switchig
    if not os.path.exists(branch_path):
        print(f"Branch {args.branch_name} does not exist.")
        return

    with open(".pit/HEAD", "w") as head:
        head.write(f"ref: refs/heads/{args.branch_name}")

    print(f"Switched to branch {args.branch_name}.")
