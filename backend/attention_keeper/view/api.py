from flask_api import FlaskAPI, status
from flask_jwt_extended import JWTManager, jwt_optional, get_current_user, get_raw_jwt, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

from attention_keeper.util import logger

db = SQLAlchemy()

LOGGER = logger.get_logger(__name__)


def create_app(config):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config)
    jwt = JWTManager(app)

    from attention_keeper.model.participant import Participant
    from attention_keeper.util.auth import create_participant_jwt

    db.init_app(app)
    with app.app_context():
        db.create_all()

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
