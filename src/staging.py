#!/usr/bin/env python3
"""
A module for managing file staging in a simple distributed source control system.

This script provides functionality to hash files and stage them for committing to the repository. 
It uses SHA-1 hashing to create a unique identifier for each file and stores them in the `.repo/objects` directory. 
The files are then listed in the `.repo/index` file for further processing in the source control system.

Functions:
- hash_file: Computes the SHA-1 hash of a file.
- add_files: Stages the specified files by adding them to the repository and updating the index.
"""

import hashlib
import os

from src.constants import PIT_DIR
from src.utils import (ensure_repo, get_repo_dir, get_staged_files,
                       split_object_hash)


def hash_file(abs_file):
    """
    Computes the SHA-1 hash of the specified file.

    Args:
        abs_file (str): The path to the file to be hashed.

    Returns:
        str: The SHA-1 hash of the file as a hexadecimal string.
    """
    with open(abs_file, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def add_files(args):
    """
     Stages files by adding them to the repository and updating the index file.

    The files specified in the `args.files` list are added to the `.pit/objects` directory
    and the `.pit/index` file is updated with the file name and its corresponding SHA-1 hash.
    If a file does not exist or the repository is not initialized, an appropriate message is printed.

    Args:
        args: The parsed command-line arguments, which include a list of files to be staged.

    Prints:
        A message indicating the files that have been staged, or errors if files are missing
        or the repository is not initialized.
    """

    # Get repo dir to enable calling the command from anypoint within the repo tree
    repo_dir = get_repo_dir()
    # Make sure repo has been initialized
    ensure_repo(repo_dir)
    # Get files already in stating
    files_in_stage = get_staged_files(repo_dir)

    staged_files = []
    with open(os.path.join(repo_dir, PIT_DIR, "index"), "a", encoding="utf-8") as index: # use absolute path
        for file in args.files:
            # Since we can run this command from anywhere within the repo tree, we need the -
            # absolute file path based on the current working dir
            abs_file = os.path.join(os.path.abspath(os.getcwd()), file)
            if not os.path.exists(abs_file):
                print(f"File {abs_file} not found.")
                continue
            # Get the relative file path (relative to base repo dir) to be able to compare with -
            # files in the repo tree
            relative_file = abs_file.split(repo_dir)[-1][1:]
            if relative_file in [i.split()[0] for i in files_in_stage]:
                if hash := hash_file(file) in [i.split()[1] for i in files_in_stage]:
                    continue
            file_hash = hash_file(abs_file)
            file_hash_folder, file_hash_name = split_object_hash(file_hash)
            file_object_dir = os.path.join(repo_dir, PIT_DIR, "objects", file_hash_folder)
            os.makedirs(file_object_dir, exist_ok=True)
            object_path = os.path.join(file_object_dir, file_hash_name)
            with open(object_path, "wb") as obj:
                with open(abs_file, "rb") as src:
                    obj.write(src.read())
            index.write(f"{relative_file} {file_hash}\n")
            staged_files.append(relative_file)
    print(f"Staged files: {', '.join(staged_files)}")
