from flask import request
from flask_api import FlaskAPI, status
from flask_jwt_extended import JWTManager, jwt_optional, get_current_user
from flask_sqlalchemy import SQLAlchemy

from attention_keeper.config import get_config
from attention_keeper.util import logger, schema_validator

LOGGER = logger.get_logger(__name__)
app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object(get_config())
db = SQLAlchemy(app)


def create_app():
    jwt = JWTManager(app)

    from attention_keeper.model.participant import Participant
    from attention_keeper.model.item import Item
    from attention_keeper.model.event import Event

    with app.app_context():
        db.create_all()

    from attention_keeper.util.auth import create_participant_jwt
    from attention_keeper.controller import event

    @jwt.user_identity_loader
    def user_identity_lookup(participant: Participant):
        return participant.participant_id

    @jwt.user_loader_callback_loader
    def user_loader_callback_loader(participant_id: int):
        if participant_id is None:
            return None
        return Participant.query.filter_by(participant_id=participant_id).first()

    @app.route('/', methods=['GET'])
    def heath():
        return "Sever is running", status.HTTP_200_OK

    @app.route('/event', methods=['POST'])
    def events():
        schema_validator.event_validator.validate(request.json)
        return event.create_event(**request.json)

    @app.route('/event/<int:event_id>', methods=['DELETE'])
    def event_endpoint(event_id: int):
        return event.delete_event(event_id)

    @app.route('/register', methods=['GET'])
    def register():
        participant = Participant(score=0)
        db.session.add(participant)
        db.session.commit()
        return create_participant_jwt(participant)

    @app.route('/question', methods=['GET', 'POST'])
    @jwt_optional
    def question():
        LOGGER.debug(get_current_user())
        return {}

    return app
