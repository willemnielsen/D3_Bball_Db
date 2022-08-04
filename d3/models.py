from d3 import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(100), unique=True, nullable=False)
    conference = db.Column(db.String(100), nullable=False)
    cityandstate = db.Column(db.String(100))
    region = db.Column(db.String(100))

    def __repr__(self):
        return f"School('{self.school}','{self.conference}')"