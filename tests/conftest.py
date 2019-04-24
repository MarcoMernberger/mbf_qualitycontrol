#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pytest
import sys
from pathlib import Path

from pypipegraph.testing.fixtures import (  # noqa:F401
    new_pipegraph,
    pytest_runtest_makereport,
)
from mbf_qualitycontrol.testing.fixtures import new_pipegraph_no_qc  # noqa: F401

root = Path(__file__).parent.parent
sys.path.append(str(root / "src"))
