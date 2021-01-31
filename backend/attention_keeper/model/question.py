from attention_keeper.view.api import db


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    prompt = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean)


class QuestionOption(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), primary_key=True, nullable=False)
    option = db.Column(db.String, primary_key=True, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
