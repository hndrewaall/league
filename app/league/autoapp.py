# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask import has_app_context
from flask.helpers import get_debug_flag

from .app import create_app
from .settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

flaskapp = create_app(CONFIG)
if not has_app_context():
    flaskapp.app_context().push()
celery = flaskapp.extensions['flask-celeryext'].celery
