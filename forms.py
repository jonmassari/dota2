from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import json

teams=[]
with open('teams.json','r', encoding='utf-8') as teams_file:
    team_json = json.load(teams_file)
    for item in team_json:
        teams.append(item['header'])

class RD2LForm(FlaskForm):
    team_select = SelectField(choices=teams)
    submit = SubmitField('Scout')