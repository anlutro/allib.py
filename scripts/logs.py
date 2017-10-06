#!/usr/bin/env python
import allib.logging
import argparse
import logging
log = logging.getLogger('scripts.log')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--colors', action='store_true')
	parser.add_argument('-j', '--json', action='store_true')
	parser.add_argument('-l', '--long-levels', action='store_true')
	args = parser.parse_args()

	allib.logging.setup_logging(
		log_level=logging.DEBUG,
		colors=args.colors,
		json=args.json,
		shorten_levels=not args.long_levels,
	)
	log.debug('debug test msg')
	log.info('info test msg')
	log.warning('warning test msg')
	log.error('error test msg')
	log.critical('critical test msg')
	try:
		raise Exception('test exception')
	except:
		log.exception('exception test msg')

if __name__ == '__main__':
	main()
