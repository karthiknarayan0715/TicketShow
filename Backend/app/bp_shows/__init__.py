from flask import Blueprint

app = Blueprint("shows", __name__, url_prefix="/shows")

from app.bp_shows import routes