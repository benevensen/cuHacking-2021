from attention_keeper.view.api import db


class Team(db.Model):
    name = db.Column(db.String, primary_key=True)
    
class Player(db.Model):
    first_name = db.Column(db.String, primary_key=True)
    last_name = db.Column(db.String, primary_key=True)
    total_pts = db.Column(db.Integer, nullable=False)
    total_goals = db.Column(db.Integer, nullable=False)
    team_name = db.Column(db.String, primary_key=True)
  
