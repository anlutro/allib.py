def guess_short_flag(long_flag):
	return '-' + long_flag.lstrip('-')[0]


def find_long_flag(flags):
	for flag in flags:
		if flag.startswith('--'):
			return flag


def guess_name(flags):
	flag = find_long_flag(flags)
	if flag:
		return flag.lstrip('-').replace('-', '_')


class Argument:
	def __init__(self, name, type=str, optional=False, multiple=False, choices=None):
		self.name = name
		self.type = type
		self.optional = optional
		self.multiple = multiple
		self.choices = choices


class Option:
	def __init__(self, *flags, name=None):
		self.flags = set(flags)
		self.name = name or guess_name(flags)
		self.default = False
		self.type = bool
		self.multiple = False

	def __repr__(self):
		return '<Option "%s" %r>' % (self.name, self.flags)


class ValueOption(Option):
	def __init__(self, *flags, name=None, default=None, type=str, multiple=False):
		super().__init__(*flags, name=name)
		self.default = default
		self.type = type
		self.multiple = multiple


class ArgumentSpec:
	def __init__(self, options=[], arguments=[]):
		self.options = []
		self.option_map = {}
		self.arguments = []
		for option in options:
			self.add_option(option)
		for argument in arguments:
			self.add_argument(argument)

	def add(self, item):
		if isinstance(item, Option):
			self.add_option(item)
		elif isinstance(item, Argument):
			self.add_argument(item)
		else:
			raise TypeError('can only add Option or Argument')

	def add_option(self, option: Option):
		self.options.append(option)
		for flag in option.flags:
			if flag in self.option_map:
				raise ValueError("flag %r already taken by %r" % (
					flag, self.option_map[flag]
				))
			self.option_map[flag] = option

	def add_argument(self, argument: Argument):
		self.arguments.append(argument)
