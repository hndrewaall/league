# -*- coding: utf-8 -*-
"""
Extensions module.

Each extension is initialized in the app factory located in app.py.
"""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_celeryext import FlaskCeleryExt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

from league.scheduler import SchedulerExtension
from league.slack_messenger import SlackMessenger

bcrypt = Bcrypt()
celery = FlaskCeleryExt()
csrf_protect = CsrfProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
messenger = SlackMessenger()
scheduler = SchedulerExtension()
