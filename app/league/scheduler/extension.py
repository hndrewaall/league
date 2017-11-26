# -*- coding: utf-8 -*-
"""Flask extension for scheduler."""

# from .scheduler import DatabaseScheduler
#
# from flask import _app_ctx_stack as stack


class SchedulerExtension(object):
    """Flask extension for scheduler."""

    def __init__(self, app=None, db=None):
        """Initialize scheduler."""
        self.app = app
        self.db = db
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        """Initialize scheduler."""
        self.db = db or self.db
        app.extensions['scheduler'] = self
    #
    # def init_scheduler(self):
    #     """Initialize scheduler."""
    #     return sqlite3.connect(current_app.config['SQLITE3_DATABASE'])
    #
    # @property
    # def scheduler(self):
    #     """Get scheduler instance."""
    #     ctx = stack.top
    #     if ctx is not None:
    #         if not hasattr(ctx, 'scheduler'):
    #             ctx.scheduler = self.init_scheduler()
    #         return ctx.scheduler
