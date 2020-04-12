from flask import request, jsonify
from sqlalchemy import or_
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


def get_many(current_user):
    notifications = Notification.query.filter(or_(Notification.recipient_id == current_user.id,
                                                  Notification.sender_id == current_user.id))
    notifications_received = [n.to_dict() for n in notifications if n.recipient_id == current_user.id]
    notifications_sent = [n.to_dict() for n in notifications if n.sender_id == current_user.id]
    output = {
        'notifications_received': notifications_received,
        'notifications_sent': notifications_sent
    }
    return jsonify({'notifications': output}), 200


def get(current_user, id):
    notification = Notification.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    if current_user.id not in [notification.sender_id, notification.recipient_id] and (not current_user.admin):
        return jsonify({'message': 'Unauthorized'}), 403
    return jsonify({'notification': notification.to_dict()}), 200


def get_many_admin(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized'}), 403
    notifications = Notification.query.all()
    output = []
    for notification in notifications:
        output.append(notification.to_dict())
    return jsonify({'notifications': output}), 200


def update(current_user, id):
    try:
        notification = Notification.query.get(id)
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        if current_user.id not in [notification.sender_id, notification.recipient_id] and (not current_user.admin):
            return jsonify({'message': 'Unauthorized'}), 403
        data = request.get_json()
        if 'message' in data:
            notification.message = data['message']
        if 'answered' in data:
            notification.answered = data['answered']
        notification.save()
        return jsonify({'message': 'Notification successfully updated'}), 200
    except Exception as e:
        return jsonify({'error': 'Bad Request'}), 400


def delete(current_user, id):
    notification = Notification.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    if current_user.id not in [notification.sender_id, notification.recipient_id] and (not current_user.admin):
        return jsonify({'message': 'Unauthorized'}), 403
    notification.destroy()
    return jsonify({'message': 'Notification successfully deleted'}), 200

