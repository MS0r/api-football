from flask import (Blueprint,redirect, url_for, jsonify, request)
import os
from json_data import load_data
from queries import querieshandler

bp = Blueprint('api',__name__,url_prefix='/api/v1')
cwd = os.getcwd()
source_path = os.path.join(cwd, 'europe-champions-league-json')
data = {}

for root, dirs, files in os.walk(source_path):
    for direc in dirs:
        data[direc] = load_data(os.path.join(source_path,direc,'cl.json'))
    break

@bp.before_app_request
def return_index():
    if data == {}: return redirect(url_for('index'))

@bp.route('/<temp>/teams')
def get_all_teams(temp):
    groups = data[temp]['Groups']
    num = 0
    response = {}
    for group in groups:
        for team in groups[group]:
            num += 1
            response.update({f'team{num}':groups[group][team]})

    return jsonify(response)

@bp.route('/<temp>/groups')
def get_groups(temp):
    response = data[temp]['Groups']
    return jsonify(response)

@bp.route('/<temp>/matchdays')
def get_matchdays(temp): 
    response = data[temp]['Matchday']
    return jsonify(response)


@bp.route('/<temp>/results')
def get_matchs_results(temp):
    '''API queries
        goals = minimum number of goals made in the game
        team = team who has played the match either local or away
        stadium = stadium where the game has been played
        day = either day of the week, month or specific day
    '''
    response = data[temp]['Matchs']

    matchgoals = request.args.get('goals')
    team = request.args.get('team')
    stadium = request.args.get('stadium')
    day = request.args.get('day')
    queries = [matchgoals, team, stadium, day]

    if queries.count(None) != 4:
        return jsonify(querieshandler(response,queries))
    else:
        return jsonify(response)
    
@bp.route('/<temp>/results/<matchday>')
def get_matchday_results(temp,matchday):
    matchs = data[temp]['Matchs']
    response = []
    for group in matchs:
        for match in matchs[group]:
            if matchday in match:
                response.append(matchs[group][match])
    return jsonify(response)

@bp.route('/<temp>/<group>/group')
def get_group(temp,group):
    response = data[temp]['Groups'][f'Group {group.upper()}']
    return jsonify(response)

@bp.route('/<temp>/<group>/results')
def get_group_results(temp,group):
    response = data[temp]['Matchs'][f'Group {group.upper()}']
    return jsonify(response)

