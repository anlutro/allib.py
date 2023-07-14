import os.path
import pytest


@pytest.fixture()
def test_files_dir():
    return os.path.join(os.path.dirname(__file__), "files")
