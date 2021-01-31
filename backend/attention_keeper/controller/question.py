from flask_api import status

from attention_keeper.model.question import Question
from attention_keeper.view.api import db


def get_question(event_id: int):
    return Question.query.filter_by(event_id=event_id).all(), status.HTTP_200_OK


def get_approved_question(event_id: int):
    return Question.query.filter_by(event_id=event_id, approved=True).all(), status.HTTP_200_OK


def approve_question(question_id: int, approved: bool):
    question = Question.query.filter_by(question_id=question_id).first()
    if question is None:
        return "Bad question_id", status.HTTP_400_BAD_REQUEST
    question.approved = approved
    db.session.add(question)
    db.session.commit()
    return "Operation successful", status.HTTP_200_OK
