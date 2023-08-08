from flask import request, jsonify
from app.Models import Venue, Screening
from app.Middlewares import VerifyJWT, isAdmin
from app.Helpers import DecodeJWT
from app import db
from app.bp_venues import app
from sqlalchemy.exc import IntegrityError

@app.route('get', methods=['GET'])
def get_venues():
    jwt = request.args.get('jwt')
    if not jwt:
        return jsonify(message='JWT not provided'), 400
    try:
        data = DecodeJWT(jwt)
    except Exception as e:
        return jsonify(message="Invalid JWT Token"), 400
    venue_id = request.args.get('id')
    if venue_id:
        venue = Venue.query.get(venue_id)
        if venue is None:
            return jsonify(message='Venue not found'), 404
        return jsonify(venue.as_dict())
    else:
        venues = Venue.query.all()
        return jsonify([venue.as_dict() for venue in venues])

@app.route('', methods=['POST'])
@VerifyJWT
@isAdmin
def create_venue():
    data = request.json
    try:
        if not (data.get('name') and data.get('place') and data.get('location') and data.get('capacity') and data.get('capacity')):
            return jsonify(message='Missing fields'), 400
        venue = Venue(**data)
        db.session.add(venue)
        db.session.commit()
        return jsonify(message='Venue created successfully')
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(message='Venue creation failed. Duplicate entry.'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Internal server error'), 500

@app.route('/edit', methods=['POST'])
@VerifyJWT
@isAdmin
def update_venue():
    data = request.json
    if not (data.get('name') and data.get('place') and data.get('location') and data.get('capacity') and data.get('capacity')):
        return jsonify(message='Missing fields'), 400
    venue = Venue.query.get(data.get('id'))
    if venue is None:
        return jsonify(message='Venue not found'), 404
    venue.name = data.get('name', venue.name)
    venue.place = data.get('place', venue.place)
    venue.location = data.get('location', venue.location)
    venue.capacity = data.get('capacity', venue.capacity)
    db.session.commit()
    return jsonify(message='Venue updated successfully')

@app.route('/delete', methods=['DELETE'])
@VerifyJWT
@isAdmin
def delete_venue():
    try: 
        venue_id = request.args.get('id')
        if not venue_id:
            return jsonify(message='Venue ID not provided'), 400
        venue = Venue.query.get(venue_id)
        if venue is None:
            return jsonify(message='Venue not found'), 400
        screenings = Screening.query.filter_by(venue_id=venue_id)
        for screening in screenings:
            db.session.delete(screening)
        db.session.delete(venue)
        db.session.commit()
        return jsonify(message='Venue deleted successfully')
    except Exception as e:
        print(e)
        return jsonify(message='Venue deletion failed'), 500