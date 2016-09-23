import pytest
import os.path

@pytest.fixture()
def test_files_dir():
	return os.path.join(os.path.dirname(__file__), 'files')
