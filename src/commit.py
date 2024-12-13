#!/usr/bin/env python3

import hashlib
import os
import time

from src.constants import PIT_DIR
from src.utils import (ensure_repo, get_current_branch, get_repo_dir,
                       get_staged_files, hash_content, hash_object, read_file,
                       split_object_hash, write_file, write_tree)

CURRENT_BRANCH = get_current_branch()
REPO_DIR = get_repo_dir()


def commit_changes(args):
    """
    Creates a commit object with the current state of the repository.
    """
    # Get repo dir to enable calling the command from anypoint within the repo tree
    repo_dir = get_repo_dir()
    # Make sure repo has been initialized
    ensure_repo(repo_dir)
    # Get files already in stating
    staged_files = get_staged_files(repo_dir)

    if not staged_files:
        print("No changes to commit.")
        return

    # Get current commit hash
    branch_file = os.path.join(REPO_DIR, PIT_DIR, "refs/heads", CURRENT_BRANCH)
    parent_hash = None
    if os.path.exists(branch_file):
        parent_hash = read_file(branch_file, "line").strip()

    print("PARENT HASH", parent_hash)

    # Write the tree object
    # tree_hash = write_tree(REPO_DIR)

    commit_data = f"commit: {time.time()}\n"
    # commit_data += f"tree {tree_hash}\n"
    if parent_hash:
        commit_data += f"parent {parent_hash}\n"
    commit_data += f"message: {args.message}\n"
    commit_data += "".join(staged_files)

    # commit_hash = hash_object(commit_data.encode("utf-8"), "commit", REPO_DIR)
    commit_hash = hashlib.sha1(commit_data.encode("utf-8")).hexdigest()

    # split commit hash into folder and filename
    commit_folder, commit_file_name = split_object_hash(commit_hash)

    # create the dir if it does not exits
    commit_dir = f"{PIT_DIR}/objects/{commit_folder}"
    os.makedirs(commit_dir, exist_ok=True)
    # write object files
    write_file(f"{commit_dir}/{commit_file_name}", commit_data)

    # write branch heads
    write_file(f"{PIT_DIR}/refs/heads/{CURRENT_BRANCH}", commit_hash)

    # clear branch index
    write_file(f"{PIT_DIR}/index", "")

    print(f"Committed changes: {commit_hash}")


def view_log(args):
    if not os.path.exists(PIT_DIR):
        print("Not a repository.")
        return

    with open(f"{PIT_DIR}/refs/heads/{CURRENT_BRANCH}", "r") as branch:
        commit_hash = branch.read().strip()

    while commit_hash:
        commit_file = f"{PIT_DIR}/objects/{commit_hash}"
        if not os.path.exists(commit_file):
            break
        with open(commit_file, "r") as commit_obj:
            print(commit_obj.read())
            # Assume parent commit hash is in the data for simplicity
            commit_hash = None  # Replace with actual parent hash retrieval
