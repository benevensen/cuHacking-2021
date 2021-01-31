import csv
import requests

from flask import request
from flask_api import FlaskAPI, status
from flask_jwt_extended import JWTManager, jwt_required, get_current_user
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
    from attention_keeper.model.question import Question,QuestionOption
    from attention_keeper.model.item import Item
    from attention_keeper.model.event import Event
    from attention_keeper.model.city import City
    
    from attention_keeper.model.nhl_model import Team, Player 

    with app.app_context():
        db.create_all()
        old_city = {city.name for city in City.query.all()}
        with open(app.config['NA_LOCATION_FILE'], newline='') as f:
            new_city = {city for sublist in csv.reader(f) for city in sublist} - old_city
        for city_name in new_city:
            db.session.add(City(name=city_name))
        db.session.commit()
        
        old_nhl_teams = {team.name for team in Team.query.all()}
        response = requests.get('https://records.nhl.com/site/api/franchise')
        json_response = response.json()
        new_nhl_teams = []
        for i in range(0,json_response['total']):
	        nhl_teams.append(json_response['data'][i]["teamPlaceName"] + " " + json_response['data'][i]["teamCommonName"])
        new_nhl_teams = new_nhl_teams - old_nhl_teams
        for nhl_team in new_nhl_teams:
            db.session.add(Team(name=nhl_team))
        db.session.commit()
        


    from attention_keeper.controller import event, question, participant
    from attention_keeper.util import question_generator

    @jwt.user_identity_loader
    def user_identity_lookup(user: Participant):
        return user.participant_id

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
        schema_validator.participant_validator.validate(request.json)
        return participant.create_participant(**request.json)

    @app.route('/question', methods=['GET', 'POST'])
    @jwt_required
    def questions():
        user = get_current_user()
        if request.method == 'GET':
            return question.get_question(user.event_id)
        else:
            schema_validator.participant_validator.validate(request.json)
            return question.approve_question(**request.json)

    @app.route('/question/approved', methods=['GET'])
    @jwt_required
    def question_approved():
        user = get_current_user()
        return question.get_approved_question(user.event_id)

    @app.route('/test', methods=['GET'])
    @jwt_required
    def test():
        user = get_current_user()
        return question_generator.query(request.json['text'], user.event_id)

    return app
