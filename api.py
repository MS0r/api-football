from flask import (Blueprint,redirect, url_for, jsonify, request)
import os
from app import load_data


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

@bp.route('/')
def teams():
    return jsonify(data)

@bp.route('/<temp>/teams')
def get_all_teams(temp):
    groups = data[temp]
    groups = groups['Groups']
    num = 0
    response = {}
    for group in groups:
        for team in groups[group]:
            num += 1
            response.update({f'team{num}':groups[group][team]})

    return jsonify(response)

@bp.route('/<temp>/groups')
def get_groups(temp):
    groups = data[temp]
    response = groups['Groups']
    return jsonify(response)

@bp.route('/<temp>/matchdays')
def get_matchdays(temp):
    matchdays = data[temp]
    response = matchdays['Matchday']
    return jsonify(response)


@bp.route('/<temp>/results')
def get_match_results(temp):
    group = request.args.get('group')
    matchs = data[temp]
    response = matchs['Matchs']
    if group != None:
        return jsonify(response[f'Group {group.upper()}'])
    else: 
        return jsonify(response)

    
