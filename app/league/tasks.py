# -*- coding: utf-8 -*-
"""Celery tasks."""
import math

from bs4 import BeautifulSoup
from celery import current_app as app
from celery.utils.log import get_task_logger
from requests import get

from league.models import Player

logger = get_task_logger(__name__)


@app.task
def hello_world():
    """Hello world task."""
    logger.info('Hello world!')
    return 'Hello world!'


@app.task
def sync_aga_data():
    """Update all local AGA data by scraping the AGA servers."""
    for player in Player.get_players():
        logger.info('Syncing AGA info for player {}'.format(player.aga_id))
        url = 'http://www.usgo.org/ratings-lookup-id?PlayerID={}'.format(
            player.aga_id)
        data = get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        columns = [col.text for col in soup.findAll('tr')[1].findAll('td')]
        if int(columns[0]) == player.aga_id:
            rating = float(columns[2])
            if rating > 0:
                rank = math.floor(rating)
            else:
                rank = math.ceil(rating)
            player.update(aga_rank=rank)

    return 'AGA data synced!'
