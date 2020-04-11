from flask import request, jsonify
from sites.exts import db
from sites.models import User, Notification


def is_invitation_valid(current_user, recipient):
    if not recipient.has_team() and current_user.is_captain():
        return True
    return False


def is_request_valid(current_user, recipient):
    if not current_user.has_team() and recipient.is_captain():
        return True
    return False


def create(current_user):
    try:
        data = request.get_json()
        recipient = User.query.get(data['recipient_id'])
        if data['type'] == "invitation":
            is_valid = is_invitation_valid(current_user, recipient)
        if data['type'] == "request":
            is_valid = is_request_valid(current_user, recipient)
        if not is_valid or (data['type'] not in ['invitation', 'request']):
            raise Exception("Invalid notification request body")
        new_notification = Notification(
            sender_id=current_user.id,
            recipient_id=recipient.id,
            type=data['type'],
            message=data['message']
        )
        new_notification.save()
        return jsonify({'message': 'New notification created!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400
