from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddTeam(FlaskForm):
    school = StringField('School *', validators=[DataRequired(), Length(min=2, max=100)])
    conference = StringField('Conference *', validators=[DataRequired(), Length(min=2, max=100)])
    cityandstate = StringField('City and State', validators=[Length(min=0, max=100)])
    region = StringField('Region', validators=[Length(min=0, max=100)])
    submit = SubmitField('Submit')


