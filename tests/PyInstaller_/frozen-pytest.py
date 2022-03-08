# -*- coding: utf-8 -*-
"""
Freeze pytest.main() with lamancha included.
"""
import sys

import pkg_resources
import pytest

pkg_resources.require("flit_symlink")
pkg_resources.require("setuptools_dual_license")
pkg_resources.require("setuptools_editable")
pkg_resources.require("setuptools_install")
pkg_resources.require("setuptools_missing_license")
pkg_resources.require("setuptools_wheel")
pkg_resources.require("lamancha")
pkg_resources.require("PyQt5")

sys.exit(pytest.main(sys.argv[1:] + ["--no-cov", "--tb=native"]))
