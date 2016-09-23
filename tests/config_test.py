import argparse
import os.path

import allib.config

def test_parse_config(test_files_dir):
	args = argparse.Namespace(config=None)
	cfg = allib.config.get_config(args, os.path.join(test_files_dir, 'config.cfg'))
	assert isinstance(cfg, dict)
	assert cfg['sec1']['foo'] == 'bar'
	assert cfg['sec1']['bar'] == 'baz'
	assert cfg['sec2']['baz'] == 'foo'
