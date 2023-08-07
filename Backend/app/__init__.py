from flask import Flask, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_qrcode import QRcode
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
qr = QRcode(app)

from app import tasks

@app.route("/", methods=['GET'])
def Root():
    return "THE SERVER IS UP AND RUNNING"

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