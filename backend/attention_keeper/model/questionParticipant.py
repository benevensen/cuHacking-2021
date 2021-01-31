from attention_keeper.view.api import db


class QuestionParticipant(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), primary_key=True, nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'), primary_key=True, nullable=False)
