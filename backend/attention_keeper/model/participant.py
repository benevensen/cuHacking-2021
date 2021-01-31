from attention_keeper.view.api import db


class Participant(db.Model):
    participant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
