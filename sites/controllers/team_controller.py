
from flask import request, jsonify
from sqlalchemy import exc
from sites.models import Team, User


def create(current_user):
    try:
        data = request.get_json()
        owner = User.query.get(data['owner_id'])
        if not owner:
            return jsonify({'error': 'User not found'}), 404
        if owner.id != current_user.id and (not current_user.admin):
            return jsonify({'message': 'Unauthorized'}), 403
        if owner.has_team():
            return jsonify({'error': 'User already have a team'}), 400
        new_team = Team(name=data['name'])
        new_team.captain_id = owner.id
        new_team.save()
        owner.team_id = new_team.id
        owner.save()
        return jsonify({'message': 'Team successfully created'}), 201
    except exc.IntegrityError:
        return jsonify({'error': 'Team name [' + data['name'] + '] already taken'}), 400
    except Exception as e:
        return jsonify({'error': 'Bad Request'}), 400

