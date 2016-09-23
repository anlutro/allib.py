from allib.testing import mock
from allib.flask import cache_busting_url_for


def test_cache_busting_url_for_with_static_url():
	def stub_url_for(endpoint, **kwargs):
		return 'static/' + kwargs['filename']
	app = mock.Mock()
	app.static_folder = '/path/to/static'
	stat_result = mock.Mock()
	stat_result.st_mtime = 1234.0
	f = cache_busting_url_for(app, stub_url_for, ['css'])
	with mock.patch('os.path.isfile', return_value=True) as isfile, \
	     mock.patch('os.stat', return_value=stat_result) as stat:
		url = f('static', filename='file.css')
		isfile.assert_called_once_with('/path/to/static/file.css')
		stat.assert_called_once_with('/path/to/static/file.css')
	assert 'static/file.1234.css' == url

def test_cache_busting_url_for_with_route_url():
	def stub_url_for(endpoint, **kwargs):
		return endpoint + '/' + kwargs['foo']
	url = cache_busting_url_for(mock.Mock(), stub_url_for)('test', foo='bar')
	assert 'test/bar' == url
