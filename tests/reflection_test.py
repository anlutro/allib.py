import allib.reflection


def test_get_argnames_all_positional():
	def f(a, b):
		pass

	args, kwargs = allib.reflection.get_fn_argnames(f)
	assert ('a', 'b') == args
	assert not kwargs


def test_get_argnames_all_keyword():
	def f(a='a', b='b'):
		pass

	args, kwargs = allib.reflection.get_fn_argnames(f)
	assert not args
	assert ('a', 'b') == kwargs


def test_get_function_mixed_positional_keyword():
	def f(a, b, c='c'):
		pass

	args, kwargs = allib.reflection.get_fn_argnames(f)
	assert ('a', 'b') == args
	assert ('c',) == kwargs


def test_get_class_method_argnames():
	class C(object):
		def f(a, b, c='c'):
			pass

	args, kwargs = allib.reflection.get_fn_argnames(C().f)
	assert ('a', 'b') == args
	assert ('c',) == kwargs
