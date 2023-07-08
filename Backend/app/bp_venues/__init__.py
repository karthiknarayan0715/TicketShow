from flask import Blueprint

app = Blueprint("venues", __name__, url_prefix="/venues")

from app.bp_venues import routes