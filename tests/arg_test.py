import pytest
from allib import arg
from allib.arg import spec


def get_cli(options=None, arguments=None):
	argspec = spec.ArgumentSpec(
		options=options or [],
		arguments=arguments or [],
	)
	return arg.CommandLineInterface(argspec)


def parse_args(args, options=None, arguments=None):
	return get_cli(
		options=options,
		arguments=arguments,
	).parse_args(args)


def test_parse():
	ret = parse_args(
		['stuff', '-f', '/etc/motd'],
		[spec.ValueOption('--file')],
		[spec.Argument('name')],
	)
	assert '/etc/motd' == ret['file']
	assert 'stuff' == ret['name']


def test_type():
	ret = parse_args(
		['-i', '1', '-f', '1.5'],
		[
			spec.ValueOption('--int', type=int),
			spec.ValueOption('--float', type=float),
		],
	)
	assert 1 == ret['int']
	assert 1.5 == ret['float']


def test_mutliple():
	ret = parse_args(
		['-v', '1', '-v', '2'],
		[spec.ValueOption('--value', multiple=True, type=int)],
	)
	assert 2 == len(ret['value'])
	assert [1, 2] == ret['value']


def test_choices():
	cli = get_cli(
		arguments=[spec.Argument('name', choices=('foobar', 'barbaz', 'bazfoo'))]
	)

	ret = cli.parse_args(['foo'])
	assert ret['name'] == 'foobar'

	ret = cli.parse_args(['bar'])
	assert ret['name'] == 'barbaz'

	with pytest.raises(ValueError):
		ret = cli.parse_args(['ba'])
