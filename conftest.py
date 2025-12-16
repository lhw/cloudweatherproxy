"""Pytest configuration for the test suite.

This module ensures `custom_components` is available on `sys.path`
so the vendored `cloudweatherproxy` package can be imported when
running `pytest` from the repository root.
"""

import os
import sys

# Ensure `custom_components` is on sys.path so tests can import the vendored package
ROOT = os.path.dirname(__file__)
CUSTOM_COMPONENTS = os.path.join(ROOT, "custom_components")
if CUSTOM_COMPONENTS not in sys.path:
    sys.path.insert(0, CUSTOM_COMPONENTS)
