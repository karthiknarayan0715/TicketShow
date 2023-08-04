from flask import Blueprint

app = Blueprint("tickets", __name__, url_prefix="/tickets")

from app.bp_tickets import routes