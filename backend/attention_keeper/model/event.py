from attention_keeper.view.api import db


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    rss_feed = db.Column(db.String, nullable=False)
    pid = db.Column(db.Integer)
