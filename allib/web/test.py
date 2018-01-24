import werkzeug.test

from . import Response


class Client(werkzeug.test.Client):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('response_wrapper', Response)
		super().__init__(*args, **kwargs)
