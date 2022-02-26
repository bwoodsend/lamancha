# -*- coding: utf-8 -*-
"""
Freeze pytest.main() with lamancha included.
"""
import sys
import lamancha

import pytest

sys.exit(pytest.main(sys.argv[1:] + ["--no-cov", "--tb=native"]))
