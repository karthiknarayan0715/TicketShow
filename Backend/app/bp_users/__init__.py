from flask import Blueprint

app = Blueprint("users", __name__, url_prefix="/users")

from app.bp_users import routes