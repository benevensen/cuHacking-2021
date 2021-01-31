from attention_keeper.view.api import db


class City(db.Model):
    name = db.Column(db.String, primary_key=True)
