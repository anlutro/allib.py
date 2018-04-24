import pytest

# the web module depends on di which uses 3.5+ features
web = pytest.importorskip('allib.web')
test = pytest.importorskip('allib.web.test')


def test_simple_app():
	app = web.Application(__name__)
	app.add_route('GET', '/', lambda req: 'hello world')
	client = test.Client(app.wsgi_app)

	resp = client.get('/')

	assert isinstance(resp, web.Response)
	assert 200 == resp.status_code
	assert b'hello world' == resp.data
