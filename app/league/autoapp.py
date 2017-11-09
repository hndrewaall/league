# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from flask_celeryext import create_celery_app

from .app import create_app
from .settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
celery = create_celery_app(app)
