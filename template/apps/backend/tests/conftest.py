"""Point the backend at an isolated temp database before the app is imported.

pytest imports conftest before collecting test modules, so setting the env var
here guarantees Settings() picks it up.
"""

import os
import tempfile

_db = os.path.join(tempfile.mkdtemp(prefix="opk-test-"), "test.db")
os.environ["APP_DATABASE_URL"] = f"sqlite:///{_db}"
