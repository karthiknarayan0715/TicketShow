from flask import Flask, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "key"

from app import workers

app.app_context().push()
cors = CORS(app)

celery = workers.celery

celery.conf.update(broker_url = 'redis://localhost:6379/1', result_backend = 'redis://localhost:6379/2')
celery.Task = workers.ContextTask

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import tasks
from app.Models import Shows, Venue
from flask import request, jsonify

@app.route("/", methods=['GET'])
def Root():
    return "THE SERVER IS UP AND RUNNING"
@app.route("/search", methods=['GET'])
def Search():
    results = {'shows': [], 'venues': []}
    query = request.args.get('query')
    shows_q = Shows.query.filter(Shows.name.contains(query)).all()
    venues_q = Venue.query.filter(Venue.name.contains(query)).all()
    print(shows_q, venues_q, query)
    shows = [show.as_dict() for show in shows_q]
    venues = [venue.as_dict() for venue in venues_q]
    print(shows, venues)
    results['shows'] = shows
    results['venues'] = venues
    return jsonify(results), 200

from app.tasks import csv_report
from flask import Response
@app.route('/generate_csv', methods=['GET'])
def generate_csv():
    venue_id = int(request.args.get('venue_id'))
    task = csv_report.apply_async(args=[venue_id])
    temp_file_path = task.get()
    if temp_file_path == None:
        return jsonify(message='No screenings yet'), 400
    with open(temp_file_path, mode='rb') as csvfile:
        csv_data = csvfile.read()

    # Send the CSV file content as a response with the correct content type
    return Response(csv_data, headers={
        'Content-Disposition': f'attachment; filename=venue_report.csv',
        'Content-Type': 'text/csv'
    })

from app.bp_users import app as users_bp
from app.bp_shows import app as venues_bp
from app.bp_venues import app as shows_bp
from app.bp_screenings import app as screenings_bp
from app.bp_tickets import app as tickets_bp

app.register_blueprint(users_bp)
app.register_blueprint(venues_bp)
app.register_blueprint(shows_bp)
app.register_blueprint(screenings_bp)
app.register_blueprint(tickets_bp)

# print(app.url_map)