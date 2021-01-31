import multiprocessing
import time

import feedparser
import psutil as psutil
from flask import current_app
from flask_api import status

from attention_keeper.model.event import Event
from attention_keeper.model.item import Item
from attention_keeper.util import logger
from attention_keeper.view.api import app
from attention_keeper.view.api import db

LOGGER = logger.get_logger(__name__)


def decode_rss(polling_frequency: int, rss_feed: str, event_id: int):
    while True:
        LOGGER.debug('polling rss feed: %s', rss_feed)
        feed = feedparser.parse(rss_feed)
        with app.app_context():
            items = Item.query.filter_by(event_id=event_id).all()
            for entry in feed['entries'][len(items):]:
                item = Item(event_id=event_id, title=entry['inception_slug'],
                            isBreak=entry['inception_break'] == 'true')
                db.session.add(item)
            db.session.commit()
        time.sleep(polling_frequency)


def create_rss_feed_process(polling_frequency: int, rss_feed: str, event_id: int) -> int:
    process = multiprocessing.Process(target=decode_rss,
                                      kwargs={'polling_frequency': polling_frequency, 'rss_feed': rss_feed,
                                              'event_id': event_id})
    process.start()
    return process.pid


def get_feeds():
    return {'rss_feeds': ''}


def create_event(rss_feed: str, name: str):
    event = Event(name=name, rss_feed=rss_feed)
    db.session.add(event)
    db.session.commit()
    event.pid = create_rss_feed_process(current_app.config['POLLING_FREQUENCY'], rss_feed, event.event_id)
    db.session.commit()
    return {"event_id": event.event_id}


def delete_event(event_id: int):
    event = Event.query.filter_by(event_id=event_id).first()
    if event is None:
        return "Bad event_id", status.HTTP_400_BAD_REQUEST
    else:
        process = psutil.Process(event.pid)
        process.kill()
        db.session.delete(event)
        db.session.commit()
        return "Operation successful", status.HTTP_200_OK
