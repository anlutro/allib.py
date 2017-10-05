import logging
import allib.logging
log = logging.getLogger('scripts.log')
allib.logging.setup_logging(log_level=logging.DEBUG, colors=True)
allib.logging.setup_logging(log_level=logging.DEBUG, colors=True)


log.debug('debug test msg')
log.info('info test msg')
log.warning('warning test msg')
log.error('error test msg')
log.critical('critical test msg')
try:
	raise Exception('test exception')
except:
	log.exception('exception test msg')
