import framework
from framework import di
import jinja2


__plugin__ = 'Jinja2Plugin'


class Jinja2Plugin(di.Plugin):
	@di.provider(singleton=True)
	def provide_jinja_loader(self, app: framework.Application) -> jinja2.BaseLoader:
		# TODO: ability to change which loader to use
		return jinja2.PackageLoader(app.name, 'templates')

	@di.provider(singleton=True)
	def provide_jinja_env(self, loader: jinja2.BaseLoader) -> jinja2.Environment:
		return jinja2.Environment(loader=loader)


@di.inject('jinja', jinja2.Environment)
class Jinja2ViewMixin:
	def render_template(self, template, **context):
		return framework.Response(
			self.jinja.get_template(template).render(**context),
			mimetype='text/html'
		)
