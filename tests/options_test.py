import pytest
from allib.options.argparser import parse_from_spec
from allib.options import spec


def get_spec(*opts_or_args):
	return spec.ArgumentSpec(*opts_or_args)


def parse_args(args, options=None, arguments=None):
	argspec = get_spec(options, arguments)
	return parse_from_spec(argspec, args)


def _parse_parameters():
	args = []
	file_variations = (
		['--file', '/etc/motd'],
		['-f', '/etc/motd'],
		['--file=/etc/motd'],
		['-f=/etc/motd'],
	)
	for verbose in ('prepend', 'no', 'append'):
		for stuff in ('prepend', 'append'):
			for variation in file_variations:
				args.append(
					(['--verbose'] if verbose == 'prepend' else []) +
					(['stuff'] if stuff == 'prepend' else []) +
					variation +
					(['--verbose'] if verbose == 'append' else []) +
					(['stuff'] if stuff == 'append' else [])
				)
	return args


@pytest.mark.parametrize('args', _parse_parameters())
def test_parse(args):
	ret = parse_args(
		args,
		[spec.Option('-v', '--verbose'), spec.ValueOption('-f', '--file')],
		[spec.Argument('name')],
	)
	assert '/etc/motd' == ret['file']
	assert 'stuff' == ret['name']


def test_type():
	ret = parse_args(
		['-i', '1', '-f', '1.5'],
		[
			spec.ValueOption('-i', '--int', type=int),
			spec.ValueOption('-f', '--float', type=float),
		],
	)
	assert 1 == ret['int']
	assert 1.5 == ret['float']


def test_mutliple():
	ret = parse_args(
		['-v', '1', '-v', '2'],
		[spec.ValueOption('-v', '--value', multiple=True, type=int)],
	)
	assert 2 == len(ret['value'])
	assert [1, 2] == ret['value']


def test_choices():
	argspec = get_spec(
		spec.Argument('name', choices=('foobar', 'barbaz', 'bazfoo'))
	)

	ret = parse_from_spec(argspec, ['foo'])
	assert ret['name'] == 'foobar'

	ret = parse_from_spec(argspec, ['bar'])
	assert ret['name'] == 'barbaz'

	with pytest.raises(ValueError):
		ret = parse_from_spec(argspec, ['ba'])


def test_force_stop_parsing_options():
	ret = parse_args(
		['--', '--foo'],
		[spec.Option('--foo')],
		[spec.Argument('name')],
	)
	assert False is ret['foo']
	assert '--foo' == ret['name']
