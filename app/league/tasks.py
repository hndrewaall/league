# -*- coding: utf-8 -*-
"""Celery tasks."""
import math

from bs4 import BeautifulSoup
from celery import current_app
from celery.utils.log import get_task_logger
from requests import get

from league.models import Player

logger = get_task_logger(__name__)


@current_app.task
def hello_world():
    """Hello world task."""
    return 'Hello world!'


@current_app.task
def sync_aga_data():
    """Update all local AGA data by scraping the AGA servers."""
    for player in Player.get_players():
        url = 'http://www.usgo.org/ratings-lookup-id?PlayerID={}'.format(
            player.aga_id)
        data = get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        columns = [col.text for col in soup.findAll('tr')[1].findAll('td')]
        logger.debug('AGA Data: {}'.format(columns))

        if not int(columns[0]) == player.aga_id:
            continue
        if columns[2] == '':
            continue

        rating = float(columns[2])
        if rating > 0:
            rank = math.floor(rating)
        else:
            rank = math.ceil(rating)

        player.update(aga_rank=rank)

    return
