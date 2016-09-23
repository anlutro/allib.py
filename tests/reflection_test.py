import allib.reflection


def test_get_fn_argnames():
	def f(a, b, c='c'):
		pass

	class C(object):
		def f(a, b, c='c'):
			pass

	c = C()
	for func in f, c.f:
		args, kwargs = allib.reflection.get_fn_argnames(f)
		assert ('a', 'b') == args
		assert ('c',) == kwargs
