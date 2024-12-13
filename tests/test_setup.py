#!/usr/bin/env python3

import os
import shutil
import tempfile
from unittest import TestCase

from src.constants import PIT_DIR


class RepoTestCase(TestCase):
    def setUp(self):
        # Create a temporary directory for the test repo
        self.test_dir = tempfile.mkdtemp()
        self.repo_dir = os.path.join(self.test_dir, PIT_DIR )
        os.chdir(self.test_dir)
    
    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)