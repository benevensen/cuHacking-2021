from attention_keeper.view.api import db


class Participant(db.Model):
    participant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
