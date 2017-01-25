import pytest
from allib.subprocess import run, CalledProcessError, TimeoutExpired


def test_simple_process():
	result = run('echo hello world')
	assert result.success
	assert 'hello world' == result.stdout


def test_failed_process():
	result = run('false')
	assert not result.success


def test_failed_process_throws_exception_when_check_true():
	with pytest.raises(CalledProcessError):
		result = run('false', check=True)


def test_timed_out_process():
	with pytest.raises(TimeoutExpired):
		result = run('sleep 1', timeout=0.1)
