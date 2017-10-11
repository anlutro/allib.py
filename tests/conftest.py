import os.path
import sys
import pytest

@pytest.fixture()
def test_files_dir():
	return os.path.join(os.path.dirname(__file__), 'files')

def pytest_ignore_collect(path, config):
	# di_test has python3-only syntax
	if path.basename == 'di_test.py' and sys.version_info < (3, 3):
		return True
