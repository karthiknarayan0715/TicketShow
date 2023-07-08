from flask import request, jsonify
from app.Models import Shows
from app.Middlewares import VerifyJWT
from app import db
from app.bp_shows import app

from sqlalchemy.exc import IntegrityError

@app.route('', methods=['GET'])
@VerifyJWT
def get_shows():
    shows = Shows.query.all()
    return jsonify([show.as_dict() for show in shows])

@app.route('', methods=['POST'])
@VerifyJWT
def create_show():
    data = request.json
    try:
        show = Shows(**data)
        db.session.add(show)
        db.session.commit()
        return jsonify(message='Show created successfully')
    except IntegrityError:
        db.session.rollback()
        return jsonify(message='Show creation failed. Duplicate entry.'), 400

@app.route('/<int:show_id>', methods=['GET'])
@VerifyJWT
def get_show(show_id):
    show = Shows.query.get(show_id)
    if show is None:
        return jsonify(message='Show not found'), 404
    return jsonify(show.as_dict())

@app.route('/<int:show_id>', methods=['PUT'])
@VerifyJWT
def update_show(show_id):
    show = Shows.query.get(show_id)
    if show is None:
        return jsonify(message='Show not found'), 404
    data = request.json
    show.venue_id = data.get('venue_id', show.venue_id)
    show.name = data.get('name', show.name)
    show.desc = data.get('desc', show.desc)
    show.rating = data.get('rating', show.rating)
    show.date = data.get('date', show.date)
    show.duration = data.get('duration', show.duration)
    show.tags = data.get('tags', show.tags)
    show.price = data.get('price', show.price)
    show.available = data.get('available', show.available)
    db.session.commit()
    return jsonify(message='Show updated successfully')

@app.route('/<int:show_id>', methods=['DELETE'])
@VerifyJWT
def delete_show(show_id):
    show = Shows.query.get(show_id)
    if show is None:
        return jsonify(message='Show not found'), 404
    db.session.delete(show)
    db.session.commit()
    return jsonify(message='Show deleted successfully')
