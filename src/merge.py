#!/usr/bin/env python3

import hashlib
import os

from src.constants import PIT_DIR
from src.utils import (ensure_repo, get_current_branch, hash_content,
                       split_object_hash, write_file)


def merge_branch(args):
    # Ensure repo exists
    ensure_repo()

    branch_path = f"{PIT_DIR}/refs/heads/{args.branch_name}"
    if not os.path.exists(branch_path):
        print(f"Branch {args.branch_name} does not exist.")
        return

    current_branch = get_current_branch()

    with open(f"{PIT_DIR}/refs/heads/{current_branch}", "r") as current:
        current_commit = current.read().strip()

    with open(branch_path, "r") as other:
        other_commit = other.read().strip()

    if current_commit == other_commit:
        print("Branches are already up to date.")
        return

    # Create a new merge commit (simplified, without conflict resolution)
    merge_message = f"Merged branch {args.branch_name} into {current_branch}."
    merge_data = f"commit: merge\nmessage: {merge_message}\nparent: {current_commit}\nparent: {other_commit}\n"
    merge_hash = hash_content(merge_data)

    merge_hash_folder, merge_hash_file = split_object_hash(merge_hash)
    merge_hash_dir = f"{PIT_DIR}/objects/{merge_hash_folder}"

    os.makedirs(merge_hash_dir, exist_ok=True)

    write_file(f"{merge_hash_dir}/{merge_hash_file}", merge_data)

    write_file(f"{PIT_DIR}/refs/heads/{current_branch}", merge_hash)

    print(
        f"Branch {args.branch_name} merged into {current_branch}. New commit: {merge_hash}"
    )
