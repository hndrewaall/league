# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from league.app import create_app
from league.scheduler import DatabaseScheduler
from league.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

flaskapp = create_app(CONFIG)

# push app context so we can reference extensions
flaskapp.app_context().push()
celery = flaskapp.extensions['flask-celeryext'].celery
Scheduler = DatabaseScheduler
