#!/usr/bin/env python3

import difflib
import os


def show_diff(args):
    if not os.path.exists(".pit"):
        print("Not a repository.")
        return

    with open(".pit/HEAD", "r", encoding="utf-8") as head:
        current_branch = head.read().strip().split(": ")[1].split("/")[-1]

    with open(f".pit/refs/heads/{current_branch}", "r", encoding="utf-8") as branch:
        latest_commit_hash = branch.read().strip()

    if not os.path.exists(f".pit/objects/{latest_commit_hash}"):
        print("No commits in the current branch.")
        return

    staged_files = []
    with open(".pit/index", "r", encoding="utf-8") as index:
        for line in index.readlines():
            file, _ = line.strip().split()
            staged_files.append(file)

    print("Comparing current working directory with latest commit:")
    for file in staged_files:
        if not os.path.exists(file):
            print(f"File {file} deleted.")
            continue

        with open(file, "r", encoding="utf-8") as f:
            working_content = f.readlines()

        commit_object_path = f".pit/objects/{latest_commit_hash}"
        with open(commit_object_path, "r", encoding="utf-8") as commit:
            for line in commit.readlines():
                if line.startswith(file):
                    _, file_hash = line.strip().split()
                    object_path = f".pit/objects/{file_hash}"
                    if os.path.exists(object_path):
                        with open(object_path, "r", encoding="utf-8") as obj:
                            committed_content = obj.readlines()

        diff = difflib.unified_diff(
            committed_content,
            working_content,
            fromfile="Committed",
            tofile="Working Directory",
        )
        print("".join(diff))
