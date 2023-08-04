from flask import Blueprint, request, jsonify
from app.Models import Venue, Screening
from app.Middlewares import VerifyJWT, isAdmin
from app.Helpers import DecodeJWT
from app import db
from app.bp_screenings import app
from sqlalchemy.exc import IntegrityError
import datetime

@app.route('/get', methods=['GET'])
def get_screenings():
    jwt = request.args.get('jwt')
    if not jwt:
        return jsonify(message='JWT not provided'), 400
    try:
        data = DecodeJWT(jwt)
    except Exception as e:
        return jsonify(message="Invalid JWT Token"), 400
    id = request.args.get('id')
    if id == None:
        screenings = Screening.query.all()
        return jsonify([screening.as_dict() for screening in screenings]), 200
    else:
        screenings = Screening.query.get(id)
        return jsonify(screenings.as_dict()), 200

@app.route('/', methods=['POST'])
@VerifyJWT
@isAdmin
def create_screening():
    data = request.json
    try:
        if not (data.get('venue_id') and data.get('show_id') and data.get('date') and data.get('time') and data.get('price')):
            return jsonify(message='Missing fields'), 400
        venue_id = data.get('venue_id')
        show_id = data.get('show_id')
        date = data.get('date')
        time = data.get('time')
        price = data.get('price')
        screening = Screening(venue_id=venue_id, show_id=show_id, date=date, time=time, price=price)
        db.session.add(screening)
        db.session.commit()
        return jsonify(message='Screening created successfully')
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(message='Screening creation failed. Duplicate entry.'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Internal server error'), 500

@app.route('/edit', methods=['POST'])
@VerifyJWT
@isAdmin
def update_screening():
    data = request.json
    if not (data.get('id') and data.get('venue_id') and data.get('show_id') and data.get('date') and data.get('time') and data.get('price')):
        return jsonify(message='Missing fields'), 400
    screening = Screening.query.get(data.get('id'))
    if screening is None:
        return jsonify(message='Screening not found'), 404
    screening.venue_id = data.get('venue_id', screening.venue_id)
    screening.show_id = data.get('show_id', screening.show_id)
    screening.date = data.get('date', screening.date)
    screening.time = data.get('time', screening.time)
    screening.price = data.get('price', screening.price)
    screening.available = data.get('available', screening.available)
    db.session.commit()
    return jsonify(message='Screening updated successfully')

@app.route('/delete', methods=['DELETE'])
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
