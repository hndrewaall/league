# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

from functools import partial

from flask import Flask, render_template, request

from league import admin, api, commands, dashboard, public
from league.assets import assets
from league.extensions import (bcrypt, cache, csrf_protect, db, debug_toolbar,
                               login_manager, messenger, migrate)
from league.public.forms import LoginForm
from league.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """
    Create application using app factory.

    See: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_before_first(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    messenger.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(dashboard.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        form = LoginForm(request.form)

        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code),
                               login_form=form), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': admin.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)


def register_before_first(app):
    """Register functions to run before first request."""
    app.before_first_request_funcs.append(
        partial(admin.utils.create_root_user, app))
    app.before_first_request_funcs.append(
        partial(admin.utils.load_messenger_config, app))
    app.before_first_request_funcs.append(
        partial(admin.utils.load_site_config, app))
