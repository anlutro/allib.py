from __future__ import absolute_import
import logging
import logging.handlers
import sys

LOG = logging.getLogger(__name__)


class ColorFormatter(logging.Formatter):
	RESET = '\033[0m'

	BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = ('\033[1;%dm' % (i + 30) for i in range(8))

	COLORS = {
		logging.DEBUG: GREEN,
		logging.INFO: BLUE,
		logging.WARNING: MAGENTA,
		logging.ERROR: YELLOW,
		logging.CRITICAL: RED,
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def format(self, record):
		if record.levelno in self.COLORS:
			record.levelname = '%s%s%s' % (
				self.COLORS[record.levelno],
				record.levelname,
				self.RESET,
			)

		return super().format(record)


def setup_logging(
	log_file=None,
	log_level=None,
	check_interactive=None,
	colors=False,
	shorten_levels=True,
):
	# shorten long level names
	if shorten_levels:
		if hasattr(logging, _levelNames):
			# python 2.7, 3.3
			logging._levelNames[logging.WARNING] = 'WARN'
			logging._levelNames['WARN'] = logging.WARNING
			logging._levelNames[logging.CRITICAL] = 'CRIT'
			logging._levelNames['CRIT'] = logging.CRITICAL
		else:
			# python 3.4+
			logging._levelToName[logging.WARNING] = 'WARN'
			logging._nameToLevel['WARN'] = logging.WARNING
			logging._levelToName[logging.CRITICAL] = 'CRIT'
			logging._nameToLevel['CRIT'] = logging.CRITICAL

	if log_level is None:
		log_level = logging.WARNING
	elif isinstance(log_level, str):
		log_level = getattr(logging, log_level.upper())
	root = logging.getLogger()
	root.setLevel(log_level)

	if not log_file or log_file.lower() == 'stderr':
		handler = logging.StreamHandler(sys.stderr)
		log_file = 'STDERR'
		check_interactive = False
	elif log_file.lower() == 'stdout':
		handler = logging.StreamHandler(sys.stdout)
		log_file = 'STDOUT'
		check_interactive = False
	elif log_file:
		handler = logging.handlers.WatchedFileHandler(log_file)
		if check_interactive is None:
			check_interactive = True

	# define the logging format
	if colors and log_file in ('STDERR', 'STDOUT'):
		log_format = '\033[37m%(asctime)s %(levelname)16s\033[37m %(name)s \033[0m%(message)s'
		formatter = ColorFormatter(log_format)
	else:
		log_format = '%(asctime)s [%(levelname)5s] [%(name)s] %(message)s'
		formatter = logging.Formatter(log_format)
	handler.setFormatter(formatter)

	# add the logging handler for all loggers
	root.addHandler(handler)

	LOG.info('set up logging to %s with level %s', log_file, log_level)

	# if logging to a file but the application is ran through an interactive
	# shell, also log to STDERR
	if check_interactive:
		if sys.__stderr__.isatty():
			console_handler = logging.StreamHandler(sys.stderr)
			if colors:
				log_format = '\033[37m%(asctime)s %(levelname)16s\033[37m %(name)s \033[0m%(message)s'
				console_handler.setFormatter(ColorFormatter(log_format))
			else:
				console_handler.setFormatter(formatter)
			root.addHandler(console_handler)
			LOG.info('set up logging to STDERR with level %s', log_level)
		else:
			LOG.info('sys.stderr is not a TTY, not logging to it')
