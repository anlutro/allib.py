from __future__ import absolute_import
import copy
import os.path


_STR_TYPES = (str, bytes)
try:
	_STR_TYPES += (unicode,) #pylint: disable=undefined-variable
except NameError:
	pass


class ConfigError(Exception):
	pass


def _merge_defaults(defaults, confdict):
	for key, value in defaults.items():
		if key not in confdict:
			confdict[key] = value
		elif isinstance(value, dict) and isinstance(confdict[key], dict):
			_merge_defaults(value, confdict[key])


def _validate_value(value, valid_type, key):
	if valid_type is str and not isinstance(value, str):
		for alt_type in _STR_TYPES:
			if isinstance(value, alt_type):
				valid_type = alt_type
				break

	if valid_type is not None and not isinstance(value, valid_type):
		msg = 'Invalid configuration value for {} - expected {}, got {}'.format(
			key, valid_type, type(value))
		raise ConfigError(msg)


def _validate_dict(confdict, types, prefix=None):
	for key, value in confdict.items():
		if key not in types:
			continue

		pkey = ('%s[%s]' % (prefix, key)) if prefix else key

		if isinstance(value, dict) and isinstance(types[key], dict):
			_validate_dict(value, types[key], pkey)
		else:
			_validate_value(value, types[key], pkey)


def _str_to_type(value, valid_type):
	if valid_type is bool:
		raise ValueError("_str_to_type shouldn't be guessing booleans!")

	if valid_type is int or valid_type is float:
		try:
			return valid_type(value)
		except ValueError:
			return value

	if valid_type is list or valid_type is tuple or valid_type is set:
		return valid_type(v.strip() for v in str(value).split(','))

	if valid_type is dict:
		pairs = [v.strip().split(':') for v in str(value).split(',')]
		value = {}
		for key, val in pairs:
			value[key.strip()] = val.strip()

	return value


def get_config(args, default_location=None, optional=True, defaults=None, types=None):
	"""
	args: A dict of command-line options
	default_location: Path to config file if not specified in `args`
	defaults: Either a dictionary of default configuration values, or a function
		that will be invoked as `defaults(config, args)` after the initial
		dictionary has been constructed.
	types: A dictionary of types to validate the config against.
	"""
	path = args.get('config') or default_location

	if not optional and not os.path.exists(path):
		msg = 'Could not find a config file at path %r' % path
		if not args.get('config'):
			msg += '. Specify one with the -c/--config command line option.'
		raise ConfigError(msg)

	def configparser_to_dict(config):
		"""
		Transform a configparser object into a dictionary.
		"""
		confdict = copy.deepcopy(defaults) if defaults else {}

		for section in config.sections():
			confdict[section] = {}
			for item, value in config.items(section):
				valid_type = None
				if types and section in types and item in types[section]:
					valid_type = types[section][item]
				if valid_type is bool:
					value = config.getboolean(section, item)
				elif valid_type:
					value = _str_to_type(value, valid_type)
					_validate_value(value, valid_type, '%s[%s]' % (section, item))
				confdict[section][item] = value

		return confdict

	def conf_file_to_dict(path):
		if path.endswith('.yml') or path.endswith('.yaml'):
			import yaml
			load = yaml.safe_load
		elif path.endswith('.json'):
			import json
			load = json.load
		elif path.endswith('.toml'):
			import toml
			load = toml.load
		else:
			try:
				import configparser
			except ImportError:
				import ConfigParser as configparser
			config = configparser.ConfigParser()
			config.read(path)
			return configparser_to_dict(config)

		with open(path) as file:
			confdict = load(file)
		if defaults:
			if callable(defaults):
				defaults(confdict, args)
			else:
				_merge_defaults(defaults, confdict)
		if types:
			_validate_dict(confdict, types)
		return confdict

	if path:
		confdict = conf_file_to_dict(path)
	else:
		if not optional:
			raise ConfigError(
				'Configuration file required! Specify one '
				'with the -c/--config command line option.'
			)
		confdict = {}

	if 'logging' not in confdict:
		confdict['logging'] = {}
	if 'log_level' in args:
		confdict['logging']['level'] = args.pop('log_level')
	if 'log_file' in args:
		confdict['logging']['file'] = args.pop('log_file')
	if 'log_path' in args:
		confdict['logging']['file'] = args.pop('log_path')

	return confdict
