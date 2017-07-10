import flask
from allib.testing import mock
from allib.flask import transform_filename, setup_cache_busting


def test_transform_filename():
	static_dir = '/path/to/static'
	stat_result = mock.Mock()
	stat_result.st_mtime = 1234.0
	with mock.patch('os.path.isfile', return_value=True) as isfile, \
	     mock.patch('os.stat', return_value=stat_result) as stat:
		url = transform_filename(static_dir, 'file.css', True)
		isfile.assert_called_once_with('/path/to/static/file.css')
		stat.assert_called_once_with('/path/to/static/file.css')
	assert 'file.1234.css' == url


def test_transform_filename_when_file_does_not_exist():
	static_dir = '/path/to/static'
	with mock.patch('os.path.isfile', return_value=False) as isfile:
		url = transform_filename(static_dir, 'file.css', True)
		isfile.assert_called_once_with('/path/to/static/file.css')
	assert 'file.css' == url


def test_app_url_defaults():
	app = flask.Flask(__name__)
	setup_cache_busting(app)
	stat_result = mock.Mock()
	stat_result.st_mtime = 1234.0
	with mock.patch('os.path.isfile', return_value=True) as isfile, \
	     mock.patch('os.stat', return_value=stat_result) as stat, \
	     app.test_request_context():
		url = flask.url_for('static', filename='file.css')
	assert '/static/file.1234.css' == url
