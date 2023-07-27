from flask import Blueprint, request, jsonify
from app.Models import Venue, Screening
from app.Middlewares import VerifyJWT, isAdmin
from app.Helpers import DecodeJWT
from app import db
from app.bp_screenings import app
from sqlalchemy.exc import IntegrityError


@app.route('/screenings', methods=['GET'])
def get_screenings():
    screenings = Screening.query.all()
    return jsonify([screening.as_dict() for screening in screenings])

@app.route('/screenings', methods=['POST'])
@VerifyJWT
@isAdmin
def create_screening():
    data = request.json
    try:
        if not (data.get('venue_id') and data.get('show_id') and data.get('date_time') and data.get('price') and data.get('available')):
            return jsonify(message='Missing fields'), 400
        screening = Screening(**data)
        db.session.add(screening)
        db.session.commit()
        return jsonify(message='Screening created successfully')
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(message='Screening creation failed. Duplicate entry.'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Internal server error'), 500

@app.route('/screenings/edit', methods=['POST'])
@VerifyJWT
@isAdmin
def update_screening():
    data = request.json
    if not (data.get('venue_id') and data.get('show_id') and data.get('date_time') and data.get('price') and data.get('available')):
        return jsonify(message='Missing fields'), 400
    screening = Screening.query.get(data.get('id'))
    if screening is None:
        return jsonify(message='Screening not found'), 404
    screening.venue_id = data.get('venue_id', screening.venue_id)
    screening.show_id = data.get('show_id', screening.show_id)
    screening.date_time = data.get('date_time', screening.date_time)
    screening.price = data.get('price', screening.price)
    screening.available = data.get('available', screening.available)
    db.session.commit()
    return jsonify(message='Screening updated successfully')

@app.route('/screenings/delete', methods=['DELETE'])
@VerifyJWT
@isAdmin
def delete_screening():
    try:
        screening_id = request.args.get('id')
        if not screening_id:
            return jsonify(message='Screening ID not provided'), 400
        screening = Screening.query.get(screening_id)
        if screening is None:
            return jsonify(message='Screening not found'), 404
        db.session.delete(screening)
        db.session.commit()
        return jsonify(message='Screening deleted successfully')
    except Exception as e:
        print(e)
        return jsonify(message='Screening deletion failed'), 500
