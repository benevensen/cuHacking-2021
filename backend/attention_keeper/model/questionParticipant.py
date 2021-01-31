from attention_keeper.view.api import db


class QuestionParticipant(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), primary_key=True, nullable=False)
