# -*- coding: utf-8 -*-

from flask import Flask, Response, request, g, \
        jsonify, redirect, url_for, flash, render_template

from flaskext.babel import Babel, gettext as _

from config import DefaultConfig
from umsw import views

DEFAULT_APP_NAME = "ums2-web-interface"

DEFAULT_MODULES = (
    (views.index, ""),
)

def create_app(config=None, app_name=None, modules=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES
    app = Flask(app_name, static_folder='umsw/statics', template_folder='umsw/templates')

    configure_app(app, config)
    configure_i18n(app)
    configure_errorhandlers(app)
    configure_modules(app, modules)

    return app


def configure_app(app, config):

    # Default configuration
    app.config.from_object(DefaultConfig())
    # Application level configuration
    if config is not None:
        app.config.from_object(config)

    # From env
    app.config.from_envvar('APP_CONFIG', silent=True)


def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES',
                                               ['en'])
        return request.accept_languages.best_match(accept_languages)


def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))


def configure_modules(app, modules):

    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)
