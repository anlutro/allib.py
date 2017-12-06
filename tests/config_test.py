import argparse
import os.path

from allib.options.config import get_config

def test_parse_config(test_files_dir):
	args = argparse.Namespace(config=None)
	cfg = get_config(args, os.path.join(test_files_dir, 'config.cfg'))
	assert isinstance(cfg, dict)
	assert cfg['sec1']['foo'] == 'bar'
	assert cfg['sec1']['bar'] == 'baz'
	assert cfg['sec2']['baz'] == 'foo'


def test_parse_yaml(test_files_dir):
	args = argparse.Namespace(config=None)
	cfg = get_config(args, os.path.join(test_files_dir, 'config.yml'))
	assert isinstance(cfg, dict)
	assert cfg['foo'] == 'bar'
	assert cfg['bar']['baz'] == 'foo'
