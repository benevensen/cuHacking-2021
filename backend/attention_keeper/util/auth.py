from datetime import timedelta
from typing import Dict

from flask_jwt_extended import create_access_token

from attention_keeper.model.participant import Participant


def create_participant_jwt(participant: Participant) -> Dict[str, str]:
    token = create_access_token(expires_delta=timedelta(0), identity=participant)
    return {'token': token}
