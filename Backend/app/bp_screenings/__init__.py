from flask import Blueprint

app = Blueprint("screenings", __name__, url_prefix="/screenings")

from app.bp_screenings import routes