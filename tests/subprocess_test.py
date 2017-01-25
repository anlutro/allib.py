import pytest
import subprocess
from allib.subprocess import run


def test_simple_process():
	result = run('echo hello world')
	assert result.success
	assert 'hello world' == result.stdout


def test_failed_process():
	result = run('false')
	assert not result.success


def test_failed_process_throws_exception_when_check_true():
	with pytest.raises(subprocess.CalledProcessError):
		result = run('false', check=True)


def test_timed_out_process():
	with pytest.raises(subprocess.TimeoutExpired):
		result = run('sleep 1', timeout=0.1)
