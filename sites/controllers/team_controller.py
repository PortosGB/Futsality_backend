from flask import request, jsonify
from sqlalchemy import exc
from sites.models import Team, User, Booking


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
        return jsonify({'message': 'Team successfully created',
                        'id': new_team.id
                        }), 201
    except exc.IntegrityError:
        return jsonify({'error': 'Team name [' + data['name'] + '] already taken'}), 400
    except Exception as e:
        return jsonify({'error': 'Bad Request'}), 400


def get(current_user, id):
    if id != current_user.team_id and (not current_user.admin):
        return jsonify({'message': 'Unauthorized'}), 403
    team = Team.query.get(id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    return jsonify({'user': team.to_dict()}), 200


# TODO remove email from user get_many when not admin (create to_dict_secure method not including private infos
def get_many(current_user):
    teams = Team.query.all()
    output = [team.to_dict() for team in teams]
    return jsonify({'teams': output}), 200


def join(current_user):
    try:
        data = request.get_json()
        team = Team.query.get(data['team_id'])
        if not team:
            return jsonify({'error': 'Team not found'}), 404
        player = User.query.get(data['player_id'])
        if not player:
            return jsonify({'error': 'User not found'}), 404
        if player.has_team():
            return jsonify({'error': 'User already have a team'}), 400
        player.team_id = team.id
        player.save()
        return jsonify({'message': "Player " + str(player.id) + " successfully added to Team " + str(team.id)}), 200
    except Exception as e:
        return jsonify({'error': 'Bad Request'}), 400


def quit_team(current_user):
    if not current_user.has_team():
        return jsonify({'error': 'User has no team'}), 400
    if current_user.is_captain():
        delete_team_bookings(current_user.team)
        current_user.team.destroy()
    current_user.team_id = None
    current_user.save()
    return jsonify({'message': 'Team successfully leaved'}), 200


def delete_team_bookings(team):
    bookings = Booking.query.filter(Booking.team_id == team.id)
    for b in bookings:
        b.destroy()
    return


def delete(current_user, id):
    try:
        team = Team.query.get(id)
        if not team:
            return jsonify({'error': 'Team not found'}), 404
        if team.captain_id != current_user.id and (not current_user.admin):
            return jsonify({'message': 'Unauthorized'}), 403
        delete_team_bookings(team)
        team.destroy()
        return jsonify({'message': 'Team successfully deleted'}), 200
    except Exception as e:
        return jsonify({'error': 'Bad Request'}), 400
