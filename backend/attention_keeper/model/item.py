from attention_keeper.view.api import db


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    title = db.Column(db.String)
    isBreak = db.Column(db.Boolean, nullable=False)
