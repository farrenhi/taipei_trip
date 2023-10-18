from flask import Blueprint

auth_obj = Blueprint('auth_obj', __name__)

from . import auth