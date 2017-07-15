from allib.data import deep_dict_merge


def test_deep_dict_merge():
	d1 = {'a': {'b': 'c'}}
	d2 = {'a': {'b': 'd', 'e': 'f'}}
	merged = deep_dict_merge(d1, d2)
	assert {'a': {'b': 'c'}} == d1
	assert {'a': {'b': 'd', 'e': 'f'}} == d2
	assert 'd' == merged['a']['b']
	assert 'f' == merged['a']['e']
