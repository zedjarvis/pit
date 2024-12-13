#!/usr/bin/env python3

import os

from src.repository import init_repo
from src.utils import read_file
from tests.test_setup import RepoTestCase


class TestRepository(RepoTestCase):
    def test_init_repo(self):
        init_repo(None)
        self.assertTrue(os.path.exists(self.repo_dir))
        self.assertTrue(os.path.exists(os.path.join(self.repo_dir, "objects")))
        self.assertTrue(os.path.exists(os.path.join(self.repo_dir, "refs/heads")))
        self.assertTrue(os.path.exists(os.path.join(self.repo_dir, "HEAD")))

        self.assertIn(
            "ref: refs/heads/master", read_file(os.path.join(self.repo_dir, "HEAD"))
        )
