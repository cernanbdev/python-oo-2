"""Shared pytest setup.

Living at the repo root, this file also puts the repo root on sys.path, so
`solution` and `publishing_app` are both importable from the tests.
"""

import pytest

from solution.seed import load_data


@pytest.fixture(autouse=True)
def fresh_data():
    """Every test starts from the same seeded objects."""
    load_data()
