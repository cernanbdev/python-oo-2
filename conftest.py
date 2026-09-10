"""Shared pytest setup.

Living at the repo root, this file also puts the repo root on sys.path, so
`publishing_app` is importable from the tests.
"""

import pytest

from publishing_app.seed import load_data


@pytest.fixture(autouse=True)
def fresh_data():
    """Every test starts from the same seeded objects."""
    load_data()
