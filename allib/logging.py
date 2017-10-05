from __future__ import absolute_import
import logging
import logging.handlers
import sys

LOG = logging.getLogger(__name__)


def get_formatter(color, shortened_levels=True):
	if color:
		level_len = 16 if shortened_levels else 19
		fmt = '\033[37m%(asctime)s %(levelname_colored)' + str(level_len) + 's\033[37m %(name)s \033[0m%(message)s'
	else:
		level_len = 5 if shortened_levels else 8
		fmt = '%(asctime)s [%(levelname)' + str(level_len) + 's] [%(name)s] %(message)s'
	return logging.Formatter(fmt)


class ColorLogRecord(logging.LogRecord):
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
		self.levelname_colored = '%s%s%s' % (
			self.COLORS[self.levelno],
			self.levelname,
			self.RESET,
		)


def setup_logging(
	log_file=None,
	log_level=None,
	check_interactive=None,
	colors=False,
	shorten_levels=True,
):
	# use custom log record class if we want colors
	if colors:
		logging.setLogRecordFactory(ColorLogRecord)

	# shorten long level names
	if shorten_levels:
		# pylint: disable=no-member
		if hasattr(logging, '_levelNames'):
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
		# pylint: enable=no-member

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
	formatter = get_formatter(
		colors and log_file in ('STDERR', 'STDOUT'),
		shortened_levels=shorten_levels,
	)
	handler.setFormatter(formatter)

	# add the logging handler for all loggers
	root.addHandler(handler)

	LOG.info('set up log handler %r to %s with level %s', handler, log_file, log_level)

	# if logging to a file but the application is ran through an interactive
	# shell, also log to STDERR
	if check_interactive:
		if sys.__stderr__.isatty():
			console_handler = logging.StreamHandler(sys.stderr)
			formatter = get_formatter(colors, shortened_levels=shorten_levels)
			console_handler.setFormatter(formatter)
			root.addHandler(console_handler)
			LOG.info('set up log handler %r to STDERR with level %s',
				console_handler, log_level)
		else:
			LOG.info('sys.stderr is not a TTY, not logging to it')
