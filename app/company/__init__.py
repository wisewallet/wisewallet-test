from flask import Blueprint

company = Blueprint('company', __name__)

from . import views
