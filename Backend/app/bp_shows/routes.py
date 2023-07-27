from flask import request, jsonify
from app.Models import Shows, Screening
from app.Middlewares import VerifyJWT, isAdmin
from app import db
from app.bp_shows import app
from app.Helpers import DecodeJWT
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

@app.route('/get', methods=['GET'])
@VerifyJWT
def get_shows():
    jwt = request.args.get('jwt')
    if not jwt:
        return jsonify(message='JWT not provided'), 400
    try:
        data = DecodeJWT(jwt)
    except Exception as e:
        return jsonify(message="Invalid JWT Token"), 400
    show_id = request.args.get('id')
    if show_id is None:
        shows = Shows.query.all()
        return jsonify([show.as_dict() for show in shows]), 200
    else:
        show = Shows.query.get(show_id)
        return jsonify(show.as_dict()), 200

@app.route('', methods=['POST'])
@VerifyJWT
@isAdmin
def create_show():
    data = request.json
    try:
        if not (data.get('name') and data.get('description') and data.get('duration') and data.get('rating')):
            return jsonify(message='Missing fields'), 400
        print(data)
        show = Shows(data.get('name'), data.get('description'), data.get('duration'), data.get('rating'))
        db.session.add(show)
        db.session.commit()
        return jsonify(message='Venue created successfully'), 200
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return jsonify(message='Venue creation failed. Duplicate entry.'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Internal server error'), 500

@app.route('/<int:show_id>', methods=['GET'])
@VerifyJWT
def get_show(show_id):
    show = Shows.query.get(show_id)
    if show is None:
        return jsonify(message='Show not found'), 404
    return jsonify(show.as_dict()), 200

@app.route('/edit', methods=['POST'])
@VerifyJWT
@isAdmin
def update_show():
    try:
        data = request.json
        show_id = data.get('id')
        show = Shows.query.get(show_id)
        print(data)
        if show is None:
            return jsonify(message='Show not found'), 400
        show.name = data.get('name')
        show.desc = data.get('description')
        show.rating = data.get('rating')
        show.duration = data.get('duration')
        print(show.desc)
        db.session.commit()
        return jsonify(message='Show updated successfully'), 200
    except Exception as e:
        print(e)
        return jsonify(message='Internal server error'), 500

@app.route('/delete', methods=['DELETE'])
@VerifyJWT
def delete_show():
    show_id = request.args.get('id')
    if not show_id:
        return jsonify(message='Show ID not provided'), 400
    show = Shows.query.get(show_id)
    if show is None:
        return jsonify(message='Show not found'), 404
    db.session.delete(show)
    db.session.commit()
    return jsonify(message='Show deleted successfully')

@app.route('/screening/<int:show_id>/<int:venue_id>', methods=['GET'])
@VerifyJWT
@isAdmin
def get_screening(show_id, venue_id):
    screening = Screening.query.filter_by(and_(venue_id=venue_id, show_id=show_id)).all()
    if not screening is None:
        return jsonify(screening.as_dict()), 200
    return jsonify(message='Screening not found'), 404

