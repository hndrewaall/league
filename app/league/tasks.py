# -*- coding: utf-8 -*-
"""Celery tasks."""
from celery import current_app


@current_app.task
def hello_world():
    """Hello world task."""
    return 'Hello world!'
