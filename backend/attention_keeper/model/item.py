from attention_keeper.view.api import db


class Item(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), primary_key=True,
                         nullable=False)
    title = db.Column(db.String)
    isBreak = db.Column(db.Boolean, nullable=False)
