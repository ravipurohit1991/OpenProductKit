"""Isolate the desktop bridge tests on a temp database.

`setdefault` cooperates with apps/backend/tests/conftest.py: whichever imports
first wins, and both point at throwaway temp files.
"""

import os
import tempfile

_db = os.path.join(tempfile.mkdtemp(prefix="opk-desktop-test-"), "test.db")
os.environ.setdefault("APP_DATABASE_URL", f"sqlite:///{_db}")
