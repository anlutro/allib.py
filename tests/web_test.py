from allib.web import Application, Response
from allib.web.test import Client


def test_simple_app():
	app = Application(__name__)
	app.add_route('GET', '/', lambda req: 'hello world')
	client = Client(app.wsgi_app)

	resp = client.get('/')

	assert isinstance(resp, Response)
	assert 200 == resp.status_code
	assert b'hello world' == resp.data
