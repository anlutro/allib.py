import math


def format_timedelta(timedelta, short=True):
	"""
	Format a timedelta into a human-readable string.
	"""
	seconds = abs(timedelta.total_seconds())
	days = max(0, math.floor(seconds / (3600 * 24)))
	seconds -= 3600 * 24 * days
	hours = max(0, math.floor(seconds / 3600))
	seconds -= 3600 * hours
	minutes = max(0, math.floor(seconds / 60))
	seconds -= 60 * minutes

	parts = []
	if days > 0:
		parts.append('%d%s' % (days, 'd' if short else ' days'))
	if hours > 0:
		parts.append('%d%s' % (hours, 'h' if short else ' hours'))
	if days == 0 and minutes > 0:
		parts.append('%d%s' % (minutes, 'm' if short else ' minutes'))
	if days == 0 and hours == 0 and seconds > 0:
		parts.append('%d%s' % (seconds, 's' if short else ' seconds'))

	return ' '.join(parts) if parts else ''
