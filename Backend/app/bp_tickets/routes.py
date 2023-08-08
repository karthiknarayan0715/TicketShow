from flask import request, jsonify, send_file
from app.Models import Ticket, Screening
from app.Middlewares import VerifyJWT, isAdmin
from app.Helpers import DecodeJWT
from app import db
from app.bp_tickets import app
from sqlalchemy.exc import IntegrityError
import qrcode
import base64
from io import BytesIO
    
@app.route('/get', methods=['GET'])
def get_tickets():
    jwt = request.args.get('jwt')
    if not jwt:
        return jsonify(message='JWT not provided'), 400
    try:
        print(jwt)
        data = DecodeJWT(jwt)
    except Exception as e:
        print(e)
        return jsonify(message="Invalid JWT Token"), 400
    ticket_id = request.args.get('ticket_id')
    screening_id = request.args.get('screening_id')
    user_id = request.args.get('user_id')
    ticket = None
    if ticket_id:
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify(message='Ticket not found'), 404
        return jsonify(ticket.as_dict())
    elif screening_id and user_id:
        ticket = Ticket.query.filter_by(screening_id = screening_id, user_id = user_id).first()
        if ticket is None:
            return jsonify(message='Ticket not found'), 404
    else:
        return jsonify(message='Parameters not valid'), 400
    qr = qrcode.make(f"localhost:5173/verify_ticket?id={ticket.id}")
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return jsonify(**ticket.as_dict(), qr_code = qr_base64)
    

@app.route('/', methods=['POST'])
@VerifyJWT
def create_ticket():
    data = request.json
    try:
        if not (data.get('screening_id') and data.get('user_id') and data.get('quantity') and data.get('quantity') > 0):
            return jsonify(message='Missing fields'), 400
        existing_ticket = Ticket.query.filter_by(screening_id = data.get('screening_id'), user_id=data.get('user_id')).first()
        if(existing_ticket):
            return jsonify(message='Ticket already exists'), 400
        screening = Screening.query.get(data.get('screening_id'))
        screening.available -= data.get('quantity')
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
def update_ticket():
    data = request.json
    if not (data.get('id') and data.get('screening_id') and data.get('user_id') and data.get('quantity')):
        return jsonify(message='Missing fields'), 400
    ticket = Ticket.query.get(data.get('id'))
    screening = Screening.query.get(data.get('screening_id'))
    if not screening:
        return jsonify('Invalid Screening ID'), 400
    screening.available += ticket.quantity
    if ticket is None:
        return jsonify(message='Ticket not found'), 404
    try:
        ticket.screening_id = data.get('screening_id', ticket.screening_id)
        ticket.user_id = data.get('user_id', ticket.user_id)
        ticket.quantity = data.get('quantity', ticket.quantity)
        screening.available -= ticket.quantity
        db.session.commit()
        return jsonify(message='Ticket updated successfully')
    except Exception as e:
        print(e)
        return jsonify(message='Server Error'), 500

@app.route('/delete', methods=['DELETE'])
@VerifyJWT
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
