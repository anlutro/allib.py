import allib.reflection

def _func(a, b, c='c'):
	pass

class C(object):
	def _func(a, b, c='c'):
		pass

def test_get_fn_argnames():
	c = C()
	for func in _func, c._func:
		args, kwargs = allib.reflection.get_fn_argnames(_func)
		assert ('a', 'b') == args
		assert ('c',) == kwargs
