from sqlalchemy import PickleType

from d3 import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

    def __repr__(self):
        return f"School('{self.school}','{self.conference}')"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    stats = db.Column(PickleType)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

