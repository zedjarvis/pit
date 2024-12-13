#!/usr/bin/env python3

import os

from src.repository import init_repo
from src.staging import add_files
from src.utils import read_file, write_file
from tests.test_setup import RepoTestCase

TEST_FILE = "test_file.txt"


class TestStaging(RepoTestCase):
    def setUp(self):
        super().setUp()
        init_repo(None)
        write_file(TEST_FILE, "Hello, world!")

    def test_add_files(self):
        add_files(type("Args", (object,), {"files": [TEST_FILE]})())
        index_path = os.path.join(self.repo_dir, "index")
        self.assertTrue(os.path.exists(index_path))

        self.assertIn(TEST_FILE, read_file(index_path))
