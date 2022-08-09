from flask import render_template, url_for, flash, redirect
import pickle
import sys
from d3 import app, d3schools, players, db
from d3.forms import AddTeam
from pretty_html_table import build_table
from d3.models import Team, Player
from flask_table import Table, Col, create_table
import os
from d3scrape import scrape


# class RenameUnpickler(pickle.Unpickler):
#     def find_class(self, module, name):
#         renamed_module = module
#         if module == "teamandpage":
#             renamed_module = "d3scrape.teamandpage"
#         return super(RenameUnpickler, self).find_class(renamed_module, name)
#
#
# def renamed_load(file_obj):
#     return RenameUnpickler(file_obj).load()
#
#
# with open('d3/teams/teams_with_players.pkl', 'rb') as file:
#     teams = renamed_load(file)
# with open('d3/teams/teams_with_players.pkl', 'wb') as file:
#     pickle.dump(teams, file)

with open('d3/teams/teams_with_players.pkl', 'rb') as file:
    teams = pickle.load(file)

db.drop_all()
db.create_all()
dbteams = []
for team in teams:
    dbteam = Team(name=team.name)
    dbplayers = []
    try:
        players = team.players
    except AttributeError:
        continue
    for player in players:
        dbplayers.append(Player(name=player.name, stats=player.stats, team_id=dbteam.id))
    dbteam.players = dbplayers
    db.session.add(dbteam)
    db.session.commit()









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
    teams = Team.query.all()
    return render_template('home.html', teams=teams)


@app.route('/addteam', methods=['GET', 'POST'])
def addteam():
    form = AddTeam()
    if form.validate_on_submit():
        flash(f'{form.school.data} was added!', 'success')
        return redirect(url_for('home'))
    return render_template('addteam.html', title='Add Team', form=form)





@app.route('/<team_name>')
def index(team_name):
    PlayerTable = create_table('PlayerTable')
    team = Team.query.filter_by(name=team_name).first()
    for player in team.players:
        player.stats['Name'] = player.name
    first_player = team.players[0]
    for stat in first_player.stats.keys():
        PlayerTable.add_column(str(stat), Col(str(stat)))
    player_stats = [player.stats for player in team.players]
    table = PlayerTable(player_stats)
    return render_template('team.html', table=table)



@app.route('/about')
def about():
    return render_template('about.html', title='About')


# @app.route('/team')
# def team():
#     return render_template('team.html',team=team, tables=playertables, title=f'{team}')



