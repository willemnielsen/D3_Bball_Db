from flask import render_template, url_for, flash, redirect
import pickle
from d3 import app, d3schools, players
from d3.forms import AddTeam
from pretty_html_table import build_table
from d3.models import Team
import os

schools = d3schools.makeDF('d3schools.txt')
tables = [schools.to_html(classes='data', columns=['School', 'City and State', 'Region', 'Conference'],
                          header="true", index=False, justify='left', border=3)]

with open('d3/tables/pandas_tables.pkl', 'rb') as file:
    team_tables = pickle.load(file)


# class Team:
#     def __init__(self, name, players=None):
#         self.name = name
#         self.players = players
#
#
# players = players.makeDF('players.txt')
# team = Team('Vassar College', players)
#
# playertables = [players.to_html(classes='players', columns=['NO.', 'NAME', 'CL.', 'POS.', 'HT.', 'WT.'],
#                           header="true", index=False, justify='left', border=3)]




@app.route('/')
@app.route('/home')
def home():
    links = team_tables
    return render_template('home.html', links=links)


@app.route('/addteam', methods=['GET', 'POST'])
def addteam():
    form = AddTeam()
    if form.validate_on_submit():
        flash(f'{form.school.data} was added!', 'success')
        return redirect(url_for('home'))
    return render_template('addteam.html', title='Add Team', form=form)


@app.route('/<team_name>')
def index(team_name):
    html_tables = [build_table(team_tables[team_name], 'blue_light')]
    return render_template('team.html', tables=html_tables)



@app.route('/about')
def about():
    return render_template('about.html', title='About')


# @app.route('/team')
# def team():
#     return render_template('team.html',team=team, tables=playertables, title=f'{team}')



