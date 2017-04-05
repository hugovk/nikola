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


class DemoBuildTest(EmptyBuildTest):
    """Test that a default build of --demo works."""

    def test_avoid_double_slash_in_rss(self):
        rss_path = os.path.join(self.target_dir, "output", "rss.xml")
        rss_data = io.open(rss_path, "r", encoding="utf8").read()
        self.assertFalse('https://example.com//' in rss_data)


if __name__ == "__main__":
    unittest.main()
