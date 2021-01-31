from typing import Iterable

from flask_api import status

from attention_keeper.model.participant import Participant
from attention_keeper.model.question import Question, QuestionOption
from attention_keeper.model.questionParticipant import QuestionParticipant
from attention_keeper.view.api import db


def get_not_approved_question(event_id: int):
    return format_questions(Question.query.filter_by(event_id=event_id, approved=None).all()), status.HTTP_200_OK


def get_approved_question(participant: Participant):
    return format_questions(
        (question for question in Question.query.filter_by(event_id=participant.event_id, approved=True).all() if
         not QuestionParticipant.query.filter_by(question_id=question.question_id,
                                                 participant_id=participant.participant_id).first())), status.HTTP_200_OK


def approve_question(question_id: int, approved: bool):
    question = Question.query.filter_by(question_id=question_id).first()
    if question is None:
        return "Bad question_id", status.HTTP_400_BAD_REQUEST
    question.approved = approved
    db.session.add(question)
    db.session.commit()
    return "Operation successful", status.HTTP_200_OK


def format_questions(questions: Iterable[Question]):
    return {'questions': [{'question_id': question.question_id, 'prompt': question.prompt,
                           'options': [question_option.option for question_option in
                                       QuestionOption.query.filter_by(question_id=question.question_id).all()]} for
                          question in questions]}


def answer(participant: Participant, question_id: int, option: str):
    question = Question.query.filter_by(question_id=question_id).first()
    if question is None:
        return "Bad question_id", status.HTTP_400_BAD_REQUEST
    if QuestionParticipant.query.filter_by(question_id=question.question_id,
                                           participant_id=participant.participant_id).first():
        return "Participant has already answered this question", status.HTTP_400_BAD_REQUEST
    options = QuestionOption.query.filter_by(question_id=question.question_id).all()
    for question_option in options:
        if question_option.option == option:
            db.session.add(QuestionParticipant(question_id=question_id, participant_id=participant.participant_id))
            if question_option.correct:
                participant.score += 1
                db.session.commit()
                return {'correct': True, 'score': participant.score}
            else:
                db.session.commit()
                return {'correct': False, 'score': participant.score}
    return "Bad option", status.HTTP_400_BAD_REQUEST
