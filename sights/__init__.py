from flask import Blueprint

sights = Blueprint('sights', __name__)

# Import views after creating the blueprint to avoid circular imports
from . import views
