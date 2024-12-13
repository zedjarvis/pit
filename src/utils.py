#!/usr/bin/env python3
"""
A set of utility functions for pit.
"""

import hashlib
import os

from src.constants import MAIN_BRANCH, NOT_A_REPO_MESSAGE, PIT_DIR


def get_repo_dir(start_dir=None):
    """
    Recursively find the root of the repository by looking for the '.pit' directory.
    To ensure calling this function only ones, every function using it must firt require
        repo_dir as a param if none is given then call this function.

    Args:
        start_dir (str): The directory to start the search from. Defaults to the current working directory.

    Returns:
        str: Path to the repository's root directory if found, else None.
    """
    if start_dir is None:
        start_dir = os.getcwd()

    current_dir = os.path.abspath(start_dir)

    # Traverse up the directory tree looking for '.repo'
    while current_dir != os.path.dirname(current_dir):
        repo_dir = os.path.join(current_dir, PIT_DIR)
        if os.path.exists(repo_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None


def ensure_repo(repo_dir=None):
    """
    Check if the current directory is a repository.
    Exit if not initialized.
    """
    repo_dir = repo_dir if repo_dir else get_repo_dir()
    if not os.path.exists(os.path.join(repo_dir, PIT_DIR)):
        print(NOT_A_REPO_MESSAGE)
        exit(1)


def hash_content(content):
    """
    Compute the SHA1 hash of the given content.
    """
    return hashlib.sha1(content.encode()).hexdigest()


def split_object_hash(hash: str):
    return hash[:2], hash[2:]


def read_file(file_path, mode=None):
    """
    Safely reads a file's content
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        if mode == "lines":
            return f.readlines()
        elif mode == "line":
            return f.readline()
        else:
            return f.read()


def write_file(file_path, content):
    """
    Safely write content to a file
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def get_current_branch(repo_dir=None):
    """
    Get the current branch from HEAD
    """
    repo_dir = repo_dir if repo_dir else get_repo_dir()
    try:
        current_ref = read_file(os.path.join(repo_dir, PIT_DIR, "HEAD"))
        return current_ref.strip().split(": ")[1].split("/")[-1]
    except Exception as e:
        return MAIN_BRANCH


def get_current_commit_hash(repo_dir=None):
    """
    Get the current branch commit hash
    """
    repo_dir = repo_dir if repo_dir else get_repo_dir()
    current_branch = get_current_branch(repo_dir)
    try:
        current_hash = read_file(os.path.join(repo_dir, "refs/heads", current_branch), "line")
    except Exception as e:
        print(e)
        os._exit(0)
    return current_hash.strip()


def get_ignored_files(repo_dir):
    """
    Parse the '.pitignore' file in the repository to get a list of files and directories to ignore.

    Args:
        repo_dir (str): The root directory of the repository.

    Returns:
        tuple: A list of patterns (file and directory names) to ignore,
               a list of directories (folder patterns).
    """
    ignore_file = os.path.join(repo_dir, ".pitignore")
    ignored_files = []
    ignored_dirs = []

    if os.path.exists(ignore_file):
        with open(ignore_file, "r", encoding="utf-8") as file:
            # Read each line and strip the extra whitespaces or newlines
            for line in file.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.endswith("/"):
                        ignored_dirs.append(line[:-1])  # Remove the trailing slash
                    else:
                        ignored_files.append(line)
    return ignored_files, ignored_dirs


def get_file_hash_from_index(repo_dir, file_path):
    """
    Get the stored hash of a file from the .pit/index.

    Args:
        repo_dir (str): The root directory of the repository.
        file_path (str): The relative path of the file to look for.

    Returns:
        str or None: The hash of the file if found in the index, or None if the file is not tracked.
    """
    index_file = os.path.join(repo_dir, ".pit", "index")

    if not os.path.exists(index_file):
        return None  # If index doesn't exist, file is not tracked

    with open(index_file, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                tracked_file, file_hash = parts
                if tracked_file == file_path:
                    return file_hash  # Return the hash if the file is found

    return None  # File not found in index


def compute_file_hash(file_path):
    """Compute the hash of a file's content."""
    hasher = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def is_file_modified(repo_dir, file_path):
    """Check if the file content is modified compared to it's last tracked version."""
    tracked_file_hash = get_file_hash_from_index(repo_dir, file_path)
    current_file_hash = compute_file_hash(os.path.join(repo_dir, file_path))

    return current_file_hash != tracked_file_hash


def get_tracked_files(repo_dir):
    """Get a list of all tracked files (staged or committed)."""
    index_file = os.path.join(repo_dir, ".pit", "index")
    tracked_files = []

    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as file:
            for line in file:
                tracked_files.append(line.split()[1])  # Extract file path from index

    return tracked_files


def get_staged_files(repo_dir, mode=None):
    """Get list of files staged for commit (in index but not committed)."""
    staged_files = []
    index_file = os.path.join(repo_dir, ".pit", "index")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as file:
            if mode == "strip":
                staged_files = [line.strip() for line in file.readlines()]
            else:
                staged_files = file.readlines()

    return staged_files


def get_modified_files(repo_dir):
    """
    Get list of files that have been modified but not staged.
    Excludes ignored files and untracked files.
    """
    modified_files = []
    ignored_files, ignored_dirs = get_ignored_files(repo_dir)
    staged_files = get_staged_files(repo_dir)  # Files already staged
    tracked_files = get_tracked_files(
        repo_dir
    )  # Files already tracked (staged or committed)

    for root, dirs, files in os.walk(repo_dir):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignored_dirs]

        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), repo_dir)
            if file_path in ignored_files or any(
                file_path.startswith(f"{d}/") for d in ignored_dirs
            ):
                continue  # Skip ignored files

            # Check if file is tracked
            if file_path in tracked_files:
                if file_path in staged_files:
                    # Compare staged version with working directory version
                    staged_hash = get_file_hash_from_index(repo_dir, file_path)
                    working_hash = compute_file_hash(os.path.join(repo_dir, file_path))
                    if working_hash != staged_hash:
                        modified_files.append(file_path)
                else:
                    # Compare committed version with working directory version
                    if is_file_modified(repo_dir, file_path):
                        modified_files.append(file_path)

    return modified_files


def get_untracked_files(repo_dir):
    """
    Get a list of untracked files, excluding staged and ignored files.
    """
    untracked_files = []
    ignored_files, ignored_dirs = get_ignored_files(repo_dir)
    staged_files = get_staged_files(repo_dir)  # Get files already staged
    tracked_files = get_tracked_files(repo_dir)  # Get files already tracked

    for root, dirs, files in os.walk(repo_dir):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignored_dirs]

        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), repo_dir)
            if file_path in ignored_files or any(
                file_path.startswith(f"{d}/") for d in ignored_dirs
            ):
                continue  # Skip ignored files and directories

            if file_path not in tracked_files and file_path not in staged_files:
                untracked_files.append(file_path)

    return untracked_files


def write_tree(repo_dir=None):
    """
    Writes a Tree object by mergin already committed files with staged files
        If file exists in prev commit tree replace it in new commit tree with staged
        Else Add. The tree is sorted alphabetically
    Returns the hash of the tree object.
    """
    repo_dir = repo_dir if repo_dir else get_repo_dir()
    tree_entries = []
    committed_entries = []
    current_branch = get_current_branch()
    staged_entries = get_staged_files(repo_dir)
    full_dir_path = os.path.join(repo_dir, dir_path)
    for entry in sorted(os.listdir(full_dir_path)):
        entry_path = os.path.join(full_dir_path, entry)
        print("ENTRY PATH : ", entry_path, entry)

        # TODO: ignore files in .pitignore if PIT_DIR in entry_path:  # skip the pit directory continue
        if PIT_DIR in entry_path:
            continue

        if os.path.isfile(entry_path):
            # write blob object
            blob_hash = write_blob(repo_dir, entry_path)
            tree_entries.append(f"100644 blob {blob_hash} {entry}")
        elif os.path.isdir(entry_path):
            # Write tree object recursively
            sub_tree_hash = write_tree(repo_dir, os.path.join(dir_path, entry))
            tree_entries.append(f"40000 tree {sub_tree_hash} {entry}")

    # create tree content
    tree_content = "\n".join(tree_entries) + "\n"
    tree_hash = hash_object(tree_content.encode(), "tree", repo_dir)
    return tree_hash


def write_blob(repo_dir, file_path):
    """
    Writes a blob object for the given file.
    Returns the hash of the blob object.
    """
    with open(file_path, "rb") as file:
        content = file.read()
    blob_hash = hash_object(content, "blob", repo_dir)


def hash_object(content, obj_type, repo_dir):
    """
    Hashes the content and stores it in the .pit/objects directory.
    Returns the hash of the content.
    """
    header = f"{obj_type} {len(content)}".encode("utf-8")
    print("header", type(header))
    print("content", type(content))
    # full_content = header + b"\x00" + content
    full_content = header + content
    obj_hash = hashlib.sha1(full_content).hexdigest()

    # Store the object in .pit/objects
    obj_dir = os.path.join(repo_dir, ".pit", "objects", obj_hash[:2])
    obj_path = os.path.join(obj_dir, obj_hash[2:])
    os.makedirs(obj_dir, exist_ok=True)
    with open(obj_path, "wb") as obj_file:
        obj_file.write(full_content)

    return obj_hash
