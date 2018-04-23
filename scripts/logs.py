#!/usr/bin/env python
from allib.logging import LogSetup
import argparse
import logging
log = logging.getLogger('scripts.log')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--colors', action='store_true')
	parser.add_argument('-f', '--log-file')
	parser.add_argument('--file-level')
	parser.add_argument('--console-level')
	parser.add_argument('-j', '--json', action='store_true')
	parser.add_argument('-l', '--long-levels', action='store_true')
	parser.add_argument('-t', '--tree', action='store_true')
	args = parser.parse_args()

	ls = LogSetup(
		shorten_levels=not args.long_levels,
		colors=args.colors,
	)
	if args.log_file:
		ls.add_file(args.log_file, args.file_level, json=args.json)
	ls.add_console(args.console_level)
	ls.finish()

	log.debug('debug test msg')
	log.info('info test msg')
	log.warning('warning test msg')
	log.error('error test msg')
	log.critical('critical test msg')
	try:
		raise Exception('test exception')
	except:
		log.exception('exception test msg')

	if args.tree:
		import logging_tree
		print()
		logging_tree.printout()

if __name__ == '__main__':
	main()
