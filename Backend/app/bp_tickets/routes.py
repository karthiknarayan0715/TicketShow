from flask import request, jsonify
from app.Models import Ticket
from app.Middlewares import VerifyJWT, isAdmin
from app.Helpers import DecodeJWT
from app import db
from app.bp_tickets import app
from sqlalchemy.exc import IntegrityError

@app.route('/get', methods=['GET'])
def get_tickets():
    jwt = request.args.get('jwt')
    if not jwt:
        return jsonify(message='JWT not provided'), 400
    try:
        data = DecodeJWT(jwt)
    except Exception as e:
        return jsonify(message="Invalid JWT Token"), 400
    ticket_id = request.args.get('id')
    if ticket_id:
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify(message='Ticket not found'), 404
        return jsonify(ticket.as_dict())
    else:
        tickets = Ticket.query.all()
        return jsonify([ticket.as_dict() for ticket in tickets])

@app.route('/create', methods=['POST'])
@VerifyJWT
def create_ticket():
    data = request.json
    try:
        if not (data.get('screening_id') and data.get('user_id') and data.get('quantity')):
            return jsonify(message='Missing fields'), 400
        ticket = Ticket(**data)
        db.session.add(ticket)
        db.session.commit()
        return jsonify(message='Ticket created successfully')
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(message='Ticket creation failed. Duplicate entry.'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Internal server error'), 500

@app.route('/edit', methods=['POST'])
@VerifyJWT
@isAdmin
def update_ticket():
    data = request.json
    if not (data.get('id') and data.get('screening_id') and data.get('user_id') and data.get('quantity')):
        return jsonify(message='Missing fields'), 400
    ticket = Ticket.query.get(data.get('id'))
    if ticket is None:
        return jsonify(message='Ticket not found'), 404
    ticket.screening_id = data.get('screening_id', ticket.screening_id)
    ticket.user_id = data.get('user_id', ticket.user_id)
    ticket.quantity = data.get('quantity', ticket.quantity)
    db.session.commit()
    return jsonify(message='Ticket updated successfully')

@app.route('/delete', methods=['DELETE'])
@VerifyJWT
@isAdmin
def delete_ticket():
    try: 
        ticket_id = request.args.get('id')
        if not ticket_id:
            return jsonify(message='Ticket ID not provided'), 400
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify(message='Ticket not found'), 400
        db.session.delete(ticket)
        db.session.commit()
        return jsonify(message='Ticket deleted successfully')
    except Exception as e:
        print(e)
        return jsonify(message='Ticket deletion failed'), 500
