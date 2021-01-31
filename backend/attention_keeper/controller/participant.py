from flask_api import status

from attention_keeper.model.participant import Participant
from attention_keeper.util.auth import create_participant_jwt
from attention_keeper.view.api import db


def create_participant(event_id: int) -> tuple[dict[str, str], int]:
    participant = Participant(score=0, event_id=event_id)
    db.session.add(participant)
    db.session.commit()
    return create_participant_jwt(participant), status.HTTP_200_OK
