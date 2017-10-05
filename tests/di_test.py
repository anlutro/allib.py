from allib import di


def test_inject_into_function():
	class A: pass
	def f(a: A): return a
	a = di.Injector().get(f)
	assert isinstance(a, A)


def test_inject_into_constructor():
	class A: pass
	class B:
		def __init__(self, a: A):
			self.a = a
	b = di.Injector().get(B)
	assert isinstance(b, B)
	assert isinstance(b.a, A)


def test_nested_inject():
	class A: pass
	class B:
		def __init__(self, a: A):
			self.a = a
	class C:
		def __init__(self, b: B):
			self.b = b
	c = di.Injector().get(C)
	assert isinstance(c, C)
	assert isinstance(c.b, B)
	assert isinstance(c.b.a, A)


def test_inject_with_decorator():
	class A: pass
	@di.inject('a', A)
	class B: pass
	b = di.Injector().get(B)
	assert isinstance(b.a, A)


def test_factory():
	class A: pass
	class B(A): pass
	class C:
		def __init__(self, a: A):
			self.a = a
	i = di.Injector()
	i.factories[A] = lambda: B()
	c = i.get(C)
	assert isinstance(c.a, B)
	assert isinstance(c.a, A)


def test_provider():
	class A:
		def __init__(self, name):
			self.name = name
	@di.provider(singleton=True)
	def f() -> A:
		return A('foo')
	i = di.Injector()
	i.register_provider(f)
	a = i.get(A)
	assert isinstance(a, A)
	assert 'foo' == a.name


def test_provider_dependencies():
	class A:
		def __init__(self, name):
			self.name = name
	class B:
		def __init__(self, a: A, name):
			self.a = a
			self.name = name
	@di.provider(singleton=True)
	def a() -> A:
		return A('a')
	@di.provider(singleton=True)
	def b(a: A) -> B:
		return B(a, 'b')
	i = di.Injector()
	i.register_provider(a)
	i.register_provider(b)
	b = i.get(B)
	assert isinstance(b, B)
	assert 'b' == b.name
	assert isinstance(b.a, A)
	assert 'a' == b.a.name


def test_module():
	class TestModule(di.Module):
		@di.provider
		def f(self) -> str:
			return 'foo'
	i = di.Injector()
	i.register_module(TestModule())
	assert 'foo' == i.get(str)
