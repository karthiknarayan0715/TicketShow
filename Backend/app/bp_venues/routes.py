from flask import request, jsonify
from app.Models import Venue
from app.Middlewares import VerifyJWT
from app import db
from app.bp_users import app
from sqlalchemy.exc import IntegrityError

@app.route('', methods=['GET'])
@VerifyJWT
def get_venues():
    venues = Venue.query.all()
    return jsonify([venue.as_dict() for venue in venues])

@app.route('', methods=['POST'])
@VerifyJWT
def create_venue():
    data = request.json
    try:
        venue = Venue(**data)
        db.session.add(venue)
        db.session.commit()
        return jsonify(message='Venue created successfully')
    except IntegrityError:
        db.session.rollback()
        return jsonify(message='Venue creation failed. Duplicate entry.'), 400

@app.route('/<int:venue_id>', methods=['GET'])
@VerifyJWT
def get_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue is None:
        return jsonify(message='Venue not found'), 404
    return jsonify(venue.as_dict())

@app.route('/<int:venue_id>', methods=['PUT'])
@VerifyJWT
def update_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue is None:
        return jsonify(message='Venue not found'), 404
    data = request.json
    venue.name = data.get('name', venue.name)
    venue.place = data.get('place', venue.place)
    venue.location = data.get('location', venue.location)
    venue.capacity = data.get('capacity', venue.capacity)
    db.session.commit()
    return jsonify(message='Venue updated successfully')

@app.route('/<int:venue_id>', methods=['DELETE'])
@VerifyJWT
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue is None:
        return jsonify(message='Venue not found'), 404
    db.session.delete(venue)
    db.session.commit()
    return jsonify(message='Venue deleted successfully')