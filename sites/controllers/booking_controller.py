from flask import request, jsonify
from sites.models import User, Team, Booking
from sqlalchemy import and_


def is_field_available(data):
    date = data['booking_date']
    hour = data['booking_start_hour']
    bookings = Booking.query.filter(and_(Booking.booking_date == date,
                                         Booking.booking_start_hour == hour))
    if len(bookings > 1):
        return False
    return True


def create(current_user):
    try:
        data = request.get_json()
        if not current_user.is_captain() and (not current_user.admin):
            return jsonify({'error': 'Unauthorized'}), 403
        if not is_field_available(data):
            return jsonify({'error': 'The field is not available at the requested time'}), 400
        new_booking = Booking(booking_date=data['booking_date'],
                              booking_start_hour=data['booking_start_hour'],
                              team_id=data['team_id']
                              )
        new_booking.side = 0
        new_booking.save()
        return jsonify({'message': 'New booking created!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def get(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    return jsonify({'user': booking.to_dict()}), 200


def get_many():
    bookings = Booking.query.all()
    output = []
    for booking in bookings:
        output.append(booking.to_dict())
    return jsonify({'bookings': output}), 200


def delete(current_user, id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    if current_user.id != booking.team_id.captain_id and (not current_user.admin):
        return jsonify({'message': 'Unauthorized'}), 403
    booking.destroy()
    return jsonify({'message': 'Notification successfully deleted'}), 200
