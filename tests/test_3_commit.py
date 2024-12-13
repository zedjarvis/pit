#!/usr/bin/env python3

import os

from src.commit import commit_changes
from src.repository import init_repo
from src.staging import add_files
from src.utils import read_file, write_file
from tests.test_setup import RepoTestCase

TEST_FILE = "test_file.txt"


class TestCommit(RepoTestCase):
    def setUp(self):
        super().setUp()
        init_repo(None)
        write_file(TEST_FILE, "Hello, World!")
        add_files(type("Args", (object,), {"files": [TEST_FILE]})())

    def test_commit_changes(self):
        commit_changes(type("Args", (object,), {"message": "First commit"})())
        master_path = os.path.join(self.repo_dir, "refs/heads/master")
        self.assertTrue(os.path.exists(master_path))

        commit_hash = read_file(master_path).strip()
        self.assertTrue(
            os.path.exists(os.path.join(self.repo_dir, "objects", commit_hash))
        )
