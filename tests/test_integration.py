# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import os
import sys

import io
import locale
import shutil
import subprocess
import tempfile
import unittest

import lxml.html
import pytest

from nikola import __main__
import nikola
import nikola.plugins.command
import nikola.plugins.command.init
import nikola.utils

from .base import BaseTestCase, cd, LocaleSupportInTesting

LocaleSupportInTesting.initialize()

class EmptyBuildTest(BaseTestCase):
    """Basic integration testcase."""

    dataname = None

    @classmethod
    def setUpClass(cls):
        """Setup a demo site."""
        # for tests that need bilingual support override language_settings
        cls.language_settings()
        cls.startdir = os.getcwd()
        cls.tmpdir = tempfile.mkdtemp()
        cls.target_dir = os.path.join(cls.tmpdir, "target")
        cls.init_command = nikola.plugins.command.init.CommandInit()
        cls.fill_site()
        cls.patch_site()
        cls.build()

    @classmethod
    def language_settings(cls):
        LocaleSupportInTesting.initialize_locales_for_testing("unilingual")

    @classmethod
    def fill_site(self):
        """Add any needed initial content."""
        self.init_command.create_empty_site(self.target_dir)
        self.init_command.create_configuration(self.target_dir)

        if self.dataname:
            src = os.path.join(os.path.dirname(__file__), 'data',
                               self.dataname)
            for root, dirs, files in os.walk(src):
                for src_name in files:
                    rel_dir = os.path.relpath(root, src)
                    dst_file = os.path.join(self.target_dir, rel_dir, src_name)
                    src_file = os.path.join(root, src_name)
                    shutil.copy2(src_file, dst_file)

    @classmethod
    def patch_site(self):
        """Make any modifications you need to the site."""

    @classmethod
    def build(self):
        """Build the site."""
        with cd(self.target_dir):
            __main__.main(["build"])

    @classmethod
    def tearDownClass(self):
        """Remove the demo site."""
        # Don't saw off the branch you're sitting on!
        os.chdir(self.startdir)
        # ignore_errors=True for windows by issue #782
        shutil.rmtree(self.tmpdir, ignore_errors=(sys.platform == 'win32'))
        # Fixes Issue #438
        try:
            del sys.modules['conf']
        except KeyError:
            pass
        # clear LocaleBorg state
        nikola.utils.LocaleBorg.reset()
        if hasattr(self.__class__, "ol"):
            delattr(self.__class__, "ol")

    def test_build(self):
        """Ensure the build did something."""
        index_path = os.path.join(
            self.target_dir, "output", "archive.html")
        self.assertTrue(os.path.isfile(index_path))

        
class DemoBuildTest(EmptyBuildTest):
    """Test that a default build of --demo works."""

    def test_avoid_double_slash_in_rss(self):
        rss_path = os.path.join(self.target_dir, "output", "rss.xml")
        rss_data = io.open(rss_path, "r", encoding="utf8").read()
        self.assertFalse('https://example.com//' in rss_data)


if __name__ == "__main__":
    unittest.main()
